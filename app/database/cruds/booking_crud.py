from sqlalchemy.orm import Session
from typing import Type

from app.database.models import BookingSession, MovieSession


def create_booking(db: Session, user_id, movie_id: int) -> BookingSession:
    """
    Создает новую бронь пользователя на сеанс.
    Проверяет существование сеанса, наличие свободных мест и отсутствие предыдущей брони.
    Уменьшает количество доступных мест и сохраняет бронь в базе.
    """
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
    """
    Возвращает список всех бронирований пользователя по user_id.
    """
    return db.query(BookingSession).filter(BookingSession.user_id == user_id).all()


def get_booking_by_id(db: Session, booking_id: int) -> BookingSession | None:
    """
    Получает бронь по её ID.
    Возвращает объект BookingSession или None, если бронь не найдена.
    """
    return db.query(BookingSession).filter(BookingSession.id == booking_id).first()


def delete_booking(db: Session, booking_id: int) -> BookingSession | None:
    """
    Удаляет бронь по ID и возвращает её.
    При удалении увеличивает количество свободных мест на сеансе.
    """
    booking = db.query(BookingSession).filter(BookingSession.id == booking_id).first()
    if booking:
        session = db.query(MovieSession).filter(MovieSession.id == booking.movie_id).first()
        if session:
            session.seats += 1  # возвращаем место
        db.delete(booking)
        db.commit()
    return booking
