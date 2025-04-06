import os
import logging
import fitz  # PyMuPDF for PDF processing
import docx  # python-docx for DOCX processing
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from openai import OpenAI
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

from employees.models import Employee

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class UploadCV(APIView):  
    parser_classes = (MultiPartParser, FormParser)

    def extract_text(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден.")
            return None
        try:
            if file_path.endswith(".pdf"):
                with fitz.open(file_path) as doc:
                    return "\n".join(page.get_text("text") for page in doc if page.get_text("text"))
            elif file_path.endswith(".docx"):
                doc = docx.Document(file_path)
                return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
        except Exception as e:
            logger.error(f"Ошибка при извлечении текста: {e}")
        return None

    def analyze_cv_with_gpt(self, text):
        if not text:
            return "Ошибка: не удалось извлечь текст из файла"

        try:
            # Initialize OpenAI client with API key from environment
            client = OpenAI(api_key=OPENAI_API_KEY)

            # Call ChatGPT API
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini as specified
                messages=[
                    {
                      "role": "system",
                      "content": "Ты HR-бот, специализирующийся на анализе резюме. Твоя задача — извлечь ключевую информацию из текста резюме и представить её в структурированном виде. Распиши все коротко и по фактам. Пожалуйста, проанализируй предоставленный текст резюме и верни результат в следующем формате:\n\n" +
                                "**Формат вывода:**\n" +
                                "1. **Персональные данные**:\n" +
                                "   - Имя: [имя кандидата]\n" +
                                "   - Email: [email кандидата]\n" +
                                "   - Телефон: [номер телефона, если указан]\n" +
                                "2. **Образование**:\n" +
                                "   - [Учебное заведение, степень, специальность, годы обучения]\n" +
                                "   - [Дополнительные курсы или сертификаты, если есть]\n" +
                                "3. **Опыт работы**:\n" +
                                "   - [Название компании, должность, период работы, краткое описание обязанностей]\n" +
                                "   - [Повторить для каждого места работы]\n" +
                                "4. **Навыки**:\n" +
                                "   - [Список ключевых навыков, упомянутых в резюме]\n" +
                                "5. **Дополнительно**:\n" +
                                "   - [Языки, хобби, достижения или другая релевантная информация]\n" +
                                "6. **Краткая оценка**:\n" +
                                "   - [Краткий комментарий о сильных сторонах кандидата и пригодности для работы]\n\n" +
                                "Если какая-либо информация отсутствует, укажи 'Не указано'. Постарайся быть точным и кратким, избегая лишних деталей. Используй только данные из предоставленного текста, не придумывай информацию."
                    },
                    {"role": "user", "content": text[:15000]},  
                ],
                max_tokens=1000,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Ошибка при анализе GPT: {e}")
            return "Ошибка анализа резюме"

    @csrf_exempt
    def post(self, request, employee_id):
        if "cv_file" not in request.FILES:
            return JsonResponse({"success": False, "error": "Файл не загружен"}, status=400)

        employee = get_object_or_404(Employee, id=employee_id)
        cv_file = request.FILES["cv_file"]

        # Сохраняем файл
        relative_path = os.path.join("cvs", cv_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb+") as destination:
            for chunk in cv_file.chunks():
                destination.write(chunk)

        employee.cv_file.name = relative_path
        employee.save()

        # Извлекаем текст и анализируем
        extracted_text = self.extract_text(file_path)
        if not extracted_text:
            return JsonResponse({"success": False, "error": "Ошибка при чтении файла"}, status=400)

        analysis_summary = self.analyze_cv_with_gpt(extracted_text)

        # Сохраняем анализ
        employee.cv_text = extracted_text
        employee.cv_analysis = analysis_summary
        employee.save()

        # Возвращаем URL файла
        cv_url = employee.cv_file.url if employee.cv_file else ""

        return JsonResponse({
            "success": True,
            "cv_text": extracted_text[:300] + "..." if extracted_text else "No text extracted",
            "summary": analysis_summary or "No AI analysis available",
            "cv_url": cv_url  # Добавляем URL файла
        }, status=200)


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Вычисляем эффективность, избегая деления на ноль
    days_employed = max((date.today() - employee.hiring_date).days, 1)
    efficiency_score = (employee.tasks_completed or 0) / days_employed

    # Разбиваем анализ CV на секции, если он есть
    analysis_sections = []
    if employee.cv_analysis and employee.cv_analysis != "Анализ недоступен":
        sections = employee.cv_analysis.split("\n\n")
        for section in sections:
            if section:
                lines = section.split("\n")
                section_title = lines[0]
                section_content = lines[1:] if len(lines) > 1 else []
                analysis_sections.append({
                    "title": section_title,
                    "content": [line.strip().replace("- ", "") for line in section_content if line.strip()]
                })

    return render(request, "employee_detail/employee_detail.html", {
        "employee": employee,
        "efficiency_score": round(efficiency_score, 2),
        "analysis_sections": analysis_sections,  # Передаём структурированный анализ
    })