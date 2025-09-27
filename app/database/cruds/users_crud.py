from sqlalchemy.orm import Session
from app.database.models import UserSession
from app.schemas import UserLogin
from typing import Type


def create_user(db: Session, session_data: UserLogin) -> UserSession:
    session = UserSession(
        username=session_data.username,
        password=session_data.password
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_user_by_username(db: Session, username: str) -> Type[UserSession] | None:
    return db.query(UserSession).filter(UserSession.username == username).first()
