from fastapi import Request, HTTPException, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime

from app.utils.check_valid import check_token, check_user
from app.utils.security import verify_password, hash_password
from app.utils.schemas import UserRegister
from app.utils.token import create_token
from app.database.session import get_db
from app.database.cruds import users_crud, booking_crud
from app.logger import logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register_user_get(request: Request):
    """
    Возвращает HTML-форму регистрации пользователя.
    Использует шаблон 'user_register.html'.
    """
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register")
async def register_user_post(
        username: Annotated[str, Form(..., description="User login")],
        password: Annotated[str, Form(..., description="User password")],
        db: Session = Depends(get_db)
) -> RedirectResponse:
    """
    Обрабатывает POST-запрос на регистрацию нового пользователя.
    Проверяет существование пользователя, хеширует пароль,
    создает запись в БД и устанавливает токен в cookie.
    """
    # проверяем, есть ли пользователь
    existing_user = users_crud.get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already registered")

    # создаем нового пользователя
    user_info = UserRegister(username=username, password=hash_password(password))
    users_crud.create_user(db, user_info)

    # создаем токен
    token = create_token(username, mode=False)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token_user", value=token, httponly=True)

    logger.info("Зарегистрировался новый пользователь")
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_user_get(request: Request):
    """
    Возвращает HTML-форму для входа пользователя.
    Использует шаблон 'user_login.html'.
    """
    return templates.TemplateResponse("user_login.html", {"request": request})


@router.post("/login")
async def login_user_post(
        username: Annotated[str, Form(..., description="User login")],
        password: Annotated[str, Form(..., description="User password")],
        db: Session = Depends(get_db)
) -> RedirectResponse:
    """
    Обрабатывает POST-запрос на вход пользователя.
    Проверяет наличие пользователя и валидность пароля,
    создает токен и устанавливает его в cookie.
    """
    # ищем пользователя
    existing_user = users_crud.get_user_by_username(db, username)
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # проверяем пароль
    if not verify_password(password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # создаем токен
    token = create_token(username, mode=False)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token_user", value=token, httponly=True)
    return response


@router.get("/logout", response_class=RedirectResponse)
async def logout_user_get() -> RedirectResponse:
    """
    Выход пользователя: удаляет токен из cookie и делает редирект на главную.
    """
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token_user")
    return response


@router.get("/profile", response_class=HTMLResponse)
async def user_profile_get(request: Request, db: Session = Depends(get_db)):
    """
    Возвращает профиль пользователя с данными и будущими бронированиями.
    Проверяет токен и существование пользователя в БД.
    Использует шаблон 'profile.html'.
    """
    # Проверяем токен и получаем username
    username_or_redirect = check_token(request, mode=False)
    if isinstance(username_or_redirect, RedirectResponse):
        return username_or_redirect
    username = username_or_redirect

    # Проверяем пользователя
    user_or_redirect = check_user(db, username)
    if isinstance(user_or_redirect, RedirectResponse):
        return user_or_redirect
    user = user_or_redirect

    # Получаем все будущие забронированные сеансы
    now = datetime.now()
    bookings = [b for b in user.bookings if b.movie.time >= now]

    # Отправляем данные в шаблон
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
            "bookings": bookings
        }
    )


@router.get("/profile/session/{booking_id}", response_class=HTMLResponse)
def session_detail(request: Request, booking_id: int, db: Session = Depends(get_db)):
    """
    Отображает детали конкретного бронирования пользователя.
    Проверяет токен, пользователя и наличие бронирования.
    Использует шаблон 'movie_detail_profile.html'.
    """
    # Проверяем токен и получаем username
    username_or_redirect = check_token(request, mode=False)
    if isinstance(username_or_redirect, RedirectResponse):
        return username_or_redirect
    username = username_or_redirect

    # Проверяем пользователя
    user_or_redirect = check_user(db, username)
    if isinstance(user_or_redirect, RedirectResponse):
        return user_or_redirect

    booking = booking_crud.get_booking_by_id(db, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return templates.TemplateResponse("movie_detail_profile.html", {"request": request, "booking": booking})
