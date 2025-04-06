import logging
import openai
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from employees.models import Employee, Task

logger = logging.getLogger(__name__)

# API-ключ OpenRouter для работы с GPT
OPENROUTER_API_KEY = "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"
openai.api_key = OPENROUTER_API_KEY


def home(request):
    return render(request, "home.html")


def aboutus(request):
    return render(request, "about.html")


@login_required
def dashboard(request):
    # Текущий пользователь — это уже объект Employee
    employee = request.user
    # Проверяем роль пользователя
    if not employee.role or employee.role.name not in ["hr", "superadmin"]:
        return render(request, "no_access.html")

    employees = Employee.objects.all()
    tasks = Task.objects.all()
    return render(request, "dashboard/dashboard.html", {"employees": employees, "tasks": tasks})


def custom_logout(request):
    logout(request)
    return render(request, "auth/logout.html")


def news(request):
    return render(request, "news.html")