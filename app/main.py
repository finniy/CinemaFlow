from fastapi import FastAPI
from uvicorn import run

from app.routers import admin_router, home_router, user_router, session_routers, book_routers
from app.utils.exception_handlers import register_exception_handlers
from app.database.session import engine
from app.database import models
from app.logger import logger

app = FastAPI(
    title="CinemaFlow",
    description="CinemaFlow is a cinema management system with admin panel.",
    version="1.0.0"
)

# Создаём таблицы в базе данных (если их ещё нет)
models.Base.metadata.create_all(bind=engine)

# Регистрируем ошибки 404 и тд
register_exception_handlers(app)
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(home_router.router, tags=["Home"])
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(session_routers.router, prefix="/session", tags=["Session"])
app.include_router(book_routers.router, prefix="/book", tags=["Book"])

if __name__ == '__main__':
    logger.info("Запуск CinemaFlow")
    run('main:app', host='127.0.0.1', port=8000)
