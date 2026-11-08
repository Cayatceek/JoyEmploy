# JoyEmploy

Система управления сотрудниками, разработанная на Django. Подходит для HR-отделов и администраторов.

## Требования
- Python 3.10+ (для Django 5.1)
- Django 5.1.6
- Git

## Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Cayatceek/JoyEmploy.git
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

В текущем `requirements.txt` отсутствует используемый приложением `django-widget-tweaks`. Дополнительно установите его:
```bash
python -m pip install django-widget-tweaks
```

### 4. Настройте базу и окружение

Проект использует PostgreSQL. Создайте базу `joyemploy` и укажите собственные параметры в `DATABASES` файла `joyemploy/settings.py`. Опубликованные настройки предназначены для разработки; не используйте их для доступного извне сервиса.
Создайте файл `.env` в корне проекта и добавьте настройки, например:
```
OPENAI_API_KEY = ваш_ключ
```

Генерация `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Примените миграции
```bash
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
├── employee_detail/    # Приложение для управления подробными данными сотрудника
├── employees/         # Приложение для модели Employee и Role
├── manage_panel/     # Приложение для управления сотрудниками
├── joyemploy/        # Основные настройки проекта
├── templates/        # Шаблоны HTML
├── simple_pages/     # Настройки отдельных страних по типу регистрации и тп.
├── .gitignore        # Исключения для Git
├── requirements.txt  # Зависимости проекта
└── README.md         # Этот файл
```

## Зависимости
- `django==5.1.6` — Фреймворк
- `django-widget-tweaks` — Удобная работа с виджетами форм

## Лицензия
Этот проект распространяется под лицензией GNU Affero General Public License v3.0 (AGPL-3.0).

JoyEmploy is free software: вы можете распространять и/или изменять его в соответствии с условиями GNU Affero General Public License, опубликованной Free Software Foundation, версии 3 или (по вашему выбору) любой более поздней версии.

Этот проект распространяется в надежде, что он будет полезен, но БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, включая подразумеваемые гарантии товарной пригодности или пригодности для определённой цели. Подробности см. в GNU Affero General Public License.

Вы должны были получить копию GNU Affero General Public License вместе с этим проектом. Если нет, см. https://www.gnu.org/licenses/.

Для получения дополнительной информации о применении AGPL к вашему проекту, посетите https://www.gnu.org/licenses/agpl-3.0.html.