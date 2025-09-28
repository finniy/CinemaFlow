from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.utils.check_valid import check_token, check_user
from app.database.cruds.booking_crud import delete_booking
from app.database.session import get_db
from app.database.cruds import movies_crud, booking_crud, users_crud
from app.utils.token import verify_token

router = APIRouter()


@router.get("/{session_id}")
async def book_session(
        request: Request,
        session_id: int,
        db: Session = Depends(get_db)
):
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

    # Проверяем, существует ли сеанс
    session = movies_crud.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Пытаемся забронировать место
    try:
        booking = booking_crud.create_booking(db, user_id=user.id, movie_id=session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Редирект на страницу с деталями брони по booking_id
    return RedirectResponse(url=f"/user/profile", status_code=303)


@router.get("/cancel/{booking_id}")
async def delete_booking(request: Request, booking_id: int, db: Session = Depends(get_db)):
    """
    Отменяет бронь по её ID и перенаправляет пользователя обратно в профиль.
    """
    # Проверяем токен и получаем username
    username_or_redirect = check_token(request, mode=False)
    if isinstance(username_or_redirect, RedirectResponse):
        return username_or_redirect

    # Пытаемся удалить бронь по booking_id
    try:
        booking_crud.delete_booking(db, booking_id)
    except ValueError:
        # Можно здесь логировать ошибку или игнорировать, если бронь не найдена
        pass

    # Редирект обратно на профиль
    return RedirectResponse(url="/user/profile", status_code=303)
