from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.config import TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY_ADMIN, SECRET_KEY_USER


def create_token(login: str, mode: bool = False) -> str:
    """
    Создаёт JWT токен для указанного логина (login)

    :return: строка JWT токена
    """
    payload = {
        "sub": login,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    if mode:
        token = jwt.encode(payload, SECRET_KEY_ADMIN, algorithm=ALGORITHM)
        return token
    token = jwt.encode(payload, SECRET_KEY_USER, algorithm=ALGORITHM)
    return token


def verify_token(token: str, mode: bool = False) -> str:
    """
    Проверяет токен и возвращает логин пользователя, если токен валидный.

    :return: логин пользователя (sub)
    :raises HTTPException: если токен просрочен или неверный
    """
    try:
        if mode:
            payload = jwt.decode(token, SECRET_KEY_ADMIN, algorithms=[ALGORITHM])
            return payload["sub"]
        payload = jwt.decode(token, SECRET_KEY_USER, algorithms=[ALGORITHM])
        return payload["sub"]

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
