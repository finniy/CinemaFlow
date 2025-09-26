# CinemaFlow - Админ панель

## Установка и настройка

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Создайте файл .env

Создайте файл `.env` в корневой папке проекта со следующим содержимым:

```
ADMINS={"login":"password"}
SECRET_KEY=your_secret_key_for_JWT
ALGORITHM=JWT_signing_algorithm
TOKEN_EXPIRE_MINUTES=token_lifetime_in_minutes
```

### 3. Запустите приложение

```bash
python main.py
```

## API Endpoints

- `GET /admin/login` - Страница входа
- `POST /admin/login` - Авторизация (возвращает токен)
- `GET /admin/panel` - Панель админа (требует токен в заголовке Authorization: Bearer <token>)
