from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

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
    # Проверяем токен пользователя
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login", status_code=303)

    try:
        username = verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login", status_code=303)

    # Получаем пользователя по username
    user = users_crud.get_user_by_username(db, username)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)

    # Проверяем, существует ли сеанс
    session = movies_crud.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Пытаемся забронировать место
    try:
        booking_crud.create_booking(db, user_id=user.id, movie_id=session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Редирект на профиль
    return RedirectResponse(url="/user/profile", status_code=303)


@router.get("/cancel/{session_id}")
async def delete_booking(request: Request, session_id: int, db: Session = Depends(get_db)):
    # Проверяем токен пользователя
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login", status_code=303)

    try:
        username = verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login", status_code=303)

    # Пытаемся удалить бронь для данного сеанса
    try:
        booking_crud.delete_booking(db, session_id - 1)
    except ValueError:
        pass

    # Редирект обратно на профиль
    return RedirectResponse(url="/user/profile", status_code=303)
