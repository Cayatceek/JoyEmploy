# JoyEmploy

Система управления сотрудниками, разработанная на Django. Подходит для HR-отделов и администраторов.

## Требования
- Python 3.8+
- Django 5.1.6
- Git

## Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Sayatttttttt/JoyEmploy.git
cd JoyEmploy
```

### 2. Создайте виртуальное окружение
```bash
python -m venv .venv
```

Активируйте его:
- На Windows:
  ```bash
  .venv\Scripts\activate
  ```
- На macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

Если файл `requirements.txt` отсутствует, установите вручную:
```bash
pip install django==5.1.6 django-widget-tweaks
```

### 4. Настройте окружение
Создайте файл `.env` в корне проекта и добавьте настройки, например:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

Генерация `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Примените миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

### 7. Запустите сервер
```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу: `http://127.0.0.1:8000/`.

## Использование
1. Войдите как суперпользователь или создайте пользователя с ролью `hr`.
2. Перейдите в раздел `/manage/` для управления сотрудниками.
3. Используйте интерфейс для добавления, редактирования или удаления сотрудников.

## Структура проекта
```
JoyEmploy/
├── employees/         # Приложение для модели Employee и Role
├── manage_panel/     # Приложение для управления сотрудниками
├── joyemploy/        # Основные настройки проекта
├── templates/        # Шаблоны HTML
├── .gitignore        # Исключения для Git
├── requirements.txt  # Зависимости проекта
└── README.md         # Этот файл
```

## Зависимости
- `django==5.1.6` — Фреймворк
- `django-widget-tweaks` — Удобная работа с виджетами форм

## Лицензия
Этот проект распространяется под лицензией MIT.