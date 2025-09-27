from sqlalchemy.orm import Session
from app.database.models import MovieSession
from app.schemas import MovieSessionFull
from typing import Type
from datetime import datetime


def create_session(db: Session, session_data: MovieSessionFull) -> MovieSession:
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
    return db.query(MovieSession).filter(MovieSession.id == session_id).first()


def delete_session(db: Session, session_id: int) -> Type[MovieSession] | None:
    session = db.query(MovieSession).filter(MovieSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session
