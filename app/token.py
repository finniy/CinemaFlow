from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.config import SECRET_KEY, TOKEN_EXPIRE_MINUTES, ALGORITHM


def create_token(login: str) -> str:
    """
    Создаёт JWT токен для указанного логина (login)

    :return: строка JWT токена
    """
    payload = {
        "sub": login,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> str:
    """
    Проверяет токен и возвращает логин пользователя, если токен валидный.

    :return: логин пользователя (sub)
    :raises HTTPException: если токен просрочен или неверный
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
