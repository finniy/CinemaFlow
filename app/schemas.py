from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class Admin(BaseModel):
    username: str = Field(
        ...,
        description="Username must contain only English letters and numbers",
    )
    password: str = Field(
        ...,
        description="Password must contain only English letters and numbers",
    )


class AdminLogin(Admin):
    class Config:
        from_attributes = True


class AdminDB(Admin):
    password: str = Field(
        ...,
        min_length=4,
        description="Password must contain only English letters and numbers",
    )


class User(BaseModel):
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
    class Config:
        from_attributes = True


class UserRegister(UserLogin):
    password: str = Field(
        ...,
        min_length=4,
        description="Password must contain only English letters and numbers",
    )


class MovieSessionForm(BaseModel):
    movie: Annotated[
        str,
        Field(..., min_length=1, description="The name of the movie")
    ]
    time: Annotated[
        datetime,
        Field(..., description="Time of the session")
    ]
    hall: Annotated[
        str,
        Field(..., min_length=1, description="The hall name")
    ]
    seats: Annotated[
        int,
        Field(..., gt=0, description="Number of seats")
    ]

    class Config:
        from_attributes = True
