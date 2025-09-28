from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует переданный пароль с использованием алгоритма Argon2."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password) -> bool:
    """Проверяет, соответствует ли обычный пароль его хешу."""
    return pwd_context.verify(plain_password, hashed_password)
