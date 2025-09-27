from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class MovieSession(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    movie = Column(String, index=True, nullable=False)
    time = Column(DateTime, index=True, nullable=False)
    hall = Column(String, index=True, nullable=False)
    seats = Column(Integer, index=True, nullable=False)

    bookings = relationship("BookingSession", back_populates="movie")


class UserSession(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, index=True, nullable=False, unique=True)

    bookings = relationship("BookingSession", back_populates="user")


class BookingSession(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    user = relationship("UserSession", back_populates="bookings")
    movie = relationship("MovieSession", back_populates="bookings")
