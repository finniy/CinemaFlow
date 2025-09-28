# 🎬 FastAPI CinemaFlow

FastAPI CinemaFlow — это полнофункциональное веб-приложение для онлайн-бронирования киносеансов, построенное с
использованием FastAPI, SQLAlchemy, SQLite и Jinja2 с Bootstrap для фронтенда.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white&labelColor=101010&logoWidth=20&color=blue" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010&logoWidth=20" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-embedded-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=101010&logoWidth=20" alt="SQLite" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-9E3F8F?style=for-the-badge&logo=alchemy&logoColor=white&labelColor=101010&logoWidth=20" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Pydantic-validation-0066CC?style=for-the-badge&logo=pydantic&logoColor=white&labelColor=101010&logoWidth=20" alt="Pydantic" />
  <img src="https://img.shields.io/badge/Jinja2-templates-B41717?style=for-the-badge&logo=jinja&logoColor=white&labelColor=101010&logoWidth=20" alt="Jinja2" />
  <img src="https://img.shields.io/badge/Bootstrap-frontend-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white&labelColor=101010&logoWidth=20" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/JWT-authentication-FFB400?style=for-the-badge&logo=jsonwebtokens&logoColor=white&labelColor=101010&logoWidth=20" alt="JWT" />
  <img src="https://img.shields.io/badge/Uvicorn-ASGI-4B8BBE?style=for-the-badge&logo=uvicorn&logoColor=white&labelColor=101010&logoWidth=20" alt="Uvicorn" />
  <img src="https://img.shields.io/badge/Logging-built--in-grey?style=for-the-badge&logo=logstash&logoColor=white&labelColor=101010&logoWidth=20" alt="Logging" />
</p>

## 🚀 Возможности

- 🎬 Управление фильмами и сеансами
- 📅 Просмотр расписания киносеансов
- 🪑 Бронирование и отмена мест
- ✅ Аутентификация и авторизация через JWT
- 👤 Личный профиль пользователя с бронированиями
- 🎨 Адаптивный интерфейс на Bootstrap + Jinja2
- 🧾 Панель администратора для управления сеансами
- ⚡ Высокая скорость работы на Uvicorn + FastAPI

# 📸 Примеры работы

## 🧾Документация

![Login screen](images/docs.png)

### 🔐 Аутентификация

![Login screen](images/login.png)

### 🔍 Общий вид

![Overview](images/home.png)
![Overview](images/booking.png)

### 📦 Создание товара

![Create product](images/admin_panel.png)

## 🧰 Технологический стек

- **Язык:** Python 3.12+
- **Фреймворк:** FastAPI
- **Асинхронность:** asyncio
- **База данных:** SQLite (через SQLAlchemy ORM)
- **Схемы данных и валидация:** Pydantic v2
- **Аутентификация:** JWT
- **Хеширование паролей:** Passlib + Bcrypt
- **Фронтенд:** Jinja2 + Bootstrap 5
- **Документация:** OpenAPI (автоматически через Swagger UI)

## 📂 Структура проекта

```
.
|   .env
|   .env.template
|   .gitignore
|   database.db
|   README.md
|   requirements.txt
|
+---app
|   |   __init__.py
|   |   config.py
|   |   logger.py
|   |   main.py
|   |
|   +---database
|   |   |   __init__.py
|   |   |   models.py
|   |   |   session.py
|   |   |
|   |   +---cruds
|   |       |   __init__.py
|   |       |   booking_crud.py
|   |       |   movies_crud.py
|   |       |   users_crud.py
|   |
|   +---routers
|   |   |   __init__.py
|   |   |   admin_router.py
|   |   |   book_routers.py
|   |   |   home_router.py
|   |   |   session_routers.py
|   |   |   user_router.py
|   |
|   +---utils
|       |   __init__.py
|       |   check_valid.py
|       |   exception_handlers.py
|       |   schemas.py
|       |   security.py
|       |   token.py
|
+---images
|       admin_panel.png
|       booking.png
|       docs.png
|       home.png
|       login.png
|
\---templates
        admin_login.html
        admin_panel.html
        error.html
        home.html
        movie_detail_home.html
        movie_detail_profile.html
        profile.html
        user_login.html
        user_register.html
```

## 📦 Установка

1. Клонируйте репозиторий

```bash
git clone https://github.com/finniy/CinemaFlow.git
cd CinemaFlow
```

2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости

```bash
pip install -r requirements.txt
```

5. Запустите бота

```bash
python main.py
```

## ⚙️ Переменные окружения

Файл `.env.template` для всех необходимых переменных.

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Свободно используй, дорабатывай и распространяй с указанием авторства.

---

## 👤 Автор

- GitHub: [@finniy](https://github.com/finniy)
- Telegram: [@fjnnjk](https://t.me/fjnnjk)

💌 Не забудьте поставить звезду ⭐ на GitHub, если вам понравился сайт! 😉