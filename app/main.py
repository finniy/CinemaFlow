from fastapi import FastAPI
from app.routers import admin_router, home_router, user_router
from app.database.session import engine
from app.database import models
from uvicorn import run

app = FastAPI(
    title="CinemaFlow",
    description="CinemaFlow is a cinema management system with admin panel."
)

# Создаём таблицы в базе данных (если их ещё нет)
models.Base.metadata.create_all(bind=engine)

app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(home_router.router, tags=["Home"])
app.include_router(user_router.router, prefix="/user", tags=["User"])

if __name__ == '__main__':
    run('main:app', host='127.0.0.1', port=8000)
