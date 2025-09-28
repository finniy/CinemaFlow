from sqlalchemy.orm import Session
from typing import Type
from datetime import datetime

from app.database.models import MovieSession
from app.utils.schemas import MovieSessionFull


def create_session(db: Session, session_data: MovieSessionFull) -> MovieSession:
    """
    Создает новый сеанс фильма в базе данных.
    Добавляет объект MovieSession в сессию, коммитит и возвращает его.
    """
    session = MovieSession(
        movie=session_data.movie,
        cinema=session_data.cinema,
        description=session_data.description,
        time=session_data.time,
        hall=session_data.hall,
        seats=session_data.seats,
        duration=session_data.duration
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_sessions(db: Session, mode: bool = False) -> list[Type[MovieSession]]:
    """
    Получает список сеансов из базы.
    Если mode=True — возвращает только будущие сеансы, отсортированные по дате.
    """
    if mode:
        now = datetime.now()
        return (
            db.query(MovieSession)
            .filter(MovieSession.time >= now)  # только будущие сеансы
            .order_by(MovieSession.time.asc())  # сортировка по дате
            .all()
        )
    return db.query(MovieSession).order_by(MovieSession.time.asc()).all()


def get_session_by_id(db: Session, session_id: int) -> Type[MovieSession] | None:
    """
    Получает сеанс по его ID.
    Возвращает объект MovieSession или None, если сеанс не найден.
    """
    return db.query(MovieSession).filter(MovieSession.id == session_id).first()


def delete_session(db: Session, session_id: int) -> Type[MovieSession] | None:
    """
    Удаляет сеанс из базы по ID.
    Возвращает удаленный объект MovieSession или None, если сеанс не найден.
    """
    session = db.query(MovieSession).filter(MovieSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session
