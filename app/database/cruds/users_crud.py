from sqlalchemy.orm import Session
from typing import Type

from app.database.models import UserSession
from app.utils.schemas import UserLogin


def create_user(db: Session, session_data: UserLogin) -> UserSession:
    """
    Создает нового пользователя в базе данных.
    Добавляет объект UserSession в сессию, коммитит и возвращает его.
    """
    session = UserSession(
        username=session_data.username,
        password=session_data.password
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_user_by_username(db: Session, username: str) -> Type[UserSession] | None:
    """
    Получает пользователя из базы по username.
    Возвращает объект UserSession или None, если пользователь не найден.
    """
    return db.query(UserSession).filter(UserSession.username == username).first()
