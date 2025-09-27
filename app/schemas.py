from pydantic import BaseModel, Field
from typing import Annotated
from datetime import time


class AdminLogin(BaseModel):
    username: Annotated[
        str,
        Field(..., description="Admin username")
    ]
    password: Annotated[
        str,
        Field(..., description="Admin password")
    ]


class MovieSessionForm(BaseModel):
    movie: Annotated[
        str,
        Field(..., min_length=1, description="The name of the movie")
    ]
    time: Annotated[
        time,
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
        orm_mode = True