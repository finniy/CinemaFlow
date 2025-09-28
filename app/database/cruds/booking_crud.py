from sqlalchemy.orm import Session
from app.database.models import BookingSession, MovieSession
from typing import Type


def create_booking(db: Session, user_id, movie_id: int) -> BookingSession:
    # Проверяем, существует ли сеанс
    session = db.query(MovieSession).filter(MovieSession.id == movie_id).first()
    if not session:
        raise ValueError("Session not found")

    # Проверяем, бронировал ли уже этот пользователь этот сеанс
    existing_booking = db.query(BookingSession).filter(
        BookingSession.user_id == user_id,
        BookingSession.movie_id == movie_id
    ).first()
    if existing_booking:
        raise ValueError("You have already booked this session")

    # Проверяем доступные места
    total_booked = len(session.bookings)
    if total_booked + 1 > session.seats:
        raise ValueError("Not enough seats available")

    # Создаём бронь
    booking = BookingSession(
        user_id=user_id,
        movie_id=movie_id
    )
    session.seats -= 1

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings_by_user(db: Session, user_id: int) -> list[Type[BookingSession]]:
    return db.query(BookingSession).filter(BookingSession.user_id == user_id).all()

def get_booking_by_id(db: Session, booking_id: int) -> BookingSession | None:
    return db.query(BookingSession).filter(BookingSession.id == booking_id).first()


def delete_booking(db: Session, booking_id: int) -> BookingSession | None:
    booking = db.query(BookingSession).filter(BookingSession.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
    return booking
