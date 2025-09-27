from sqlalchemy.orm import Session
from app.database.models import MovieSession
from app.schemas import MovieSessionForm


def create_session(db: Session, session_data: MovieSessionForm):
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


def get_sessions(db: Session):
    return db.query(MovieSession).all()


def get_session_by_id(db: Session, session_id: int):
    return db.query(MovieSession).filter(MovieSession.id == session_id).first()


def delete_session(db: Session, session_id: int):
    session = db.query(MovieSession).filter(MovieSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session
