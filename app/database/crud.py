from sqlalchemy.orm import Session
from app.database.models import MovieSession
from app.schemas import MovieSessionForm
from typing import Type


def create_session(db: Session, session_data: MovieSessionForm) -> MovieSession:
    session = MovieSession(
        movie=session_data.movie,
        time=session_data.time,
        hall=session_data.hall,
        seats=session_data.seats
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_sessions(db: Session) -> list[Type[MovieSession]]:
    return db.query(MovieSession).all()


def get_session_by_id(db: Session, session_id: int) -> Type[MovieSession] | None:
    return db.query(MovieSession).filter(MovieSession.id == session_id).first()


def delete_session(db: Session, session_id: int) -> Type[MovieSession] | None:
    session = db.query(MovieSession).filter(MovieSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session

