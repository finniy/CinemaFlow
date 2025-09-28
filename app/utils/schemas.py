from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class Admin(BaseModel):
    """
    Базовая схема для администратора.
    Содержит username и password с описаниями.
    """
    username: str = Field(
        ...,
        description="Username must contain only English letters and numbers",
    )
    password: str = Field(
        ...,
        description="Password must contain only English letters and numbers",
    )


class AdminLogin(Admin):
    """
    Схема для входа администратора.
    Наследует Admin, поддерживает загрузку из ORM объектов.
    """

    class Config:
        from_attributes = True


class AdminDB(Admin):
    """
    Схема администратора в базе данных.
    Пароль имеет минимальную длину.
    """
    password: str = Field(
        ...,
        min_length=4,
        description="Password must contain only English letters and numbers",
    )


class User(BaseModel):
    """
    Базовая схема для пользователя.
    Содержит username и password с ограничениями по длине и шаблону.
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=12,
        pattern=r'^[a-zA-Z]+$',
        description="Username must contain only English letters and numbers",
    )
    password: str = Field(
        ...,
        min_length=4,
        max_length=20,
        pattern=r'^[a-zA-Z0-9]+$',
        description="Password must contain only English letters and numbers",
    )


class UserLogin(User):
    """
    Схема для входа пользователя.
    Наследует User и поддерживает загрузку из ORM объектов.
    """

    class Config:
        from_attributes = True


class UserRegister(UserLogin):
    """
    Схема для регистрации пользователя.
    Пароль дополнительно проверяется по длине.
    """
    password: str = Field(
        ...,
        min_length=4,
        description="Password must contain only English letters and numbers",
    )


# Базовый класс с общими полями
class MovieSessionBase(BaseModel):
    """
    Базовая схема для сеанса фильма.
    Общие поля: название фильма, кинотеатр, время начала.
    """
    movie: Annotated[
        str,
        Field(..., min_length=1, description="The name of the movie")
    ]
    cinema: Annotated[
        str,
        Field(..., min_length=1, description="The cinema name")
    ]
    time: Annotated[
        datetime, Field(..., description="Time of start the session")
    ]

    class Config:
        from_attributes = True


# Класс для создания сеанса (админ-панель)
class MovieSessionFull(MovieSessionBase):
    """
    Полная схема для создания или управления сеансом.
    Включает зал, количество мест, длительность и описание фильма.
    """
    hall: Annotated[
        str,
        Field(..., min_length=1, description="The hall name")
    ]
    seats: Annotated[
        int,
        Field(..., gt=0, description="Number of seats")
    ]
    duration: Annotated[
        int,
        Field(..., gt=0, description="Duration of the session in minutes")
    ]
    description: Annotated[
        str,
        Field(None, max_length=2000, description="Description of the movie")
    ]
