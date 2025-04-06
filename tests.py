import openai

client = openai.OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"  # OpenRouter API URL
)


# Используем доступную бесплатную модель
# model_name = "google/gemini-2.0-pro-exp-02-05:free"  # Проверь актуальные модели 
# model_name = "gemini v2 model - google/gemini-2.0-pro-exp-02-05:free"
model_name = "cognitivecomputations/dolphin3.0-mistral-24b:free"

completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "Ты HR-бот. Извлеки полезные данные из резюме."},
        {"role": "user", "content": "hi"}
    ],
    max_tokens=500  # Уменьшаем расход токенов
)

# Проверяем, есть ли в ответе данные
if completion.choices:
    print(completion.choices[0].message.content)
else:
    print("❌ API не вернул ожидаемый ответ:", completion)