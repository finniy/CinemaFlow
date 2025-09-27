from sqlalchemy import Column, Integer, String, Time
from app.database.session import Base


class MovieSession(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    movie = Column(String, index=True, nullable=False)
    time = Column(Time, index=True, nullable=False)
    hall = Column(String, index=True, nullable=False)
    seats = Column(Integer, index=True, nullable=False)
