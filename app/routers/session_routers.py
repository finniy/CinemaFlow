from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.models import BookingSession

from app.database.session import get_db
from app.database.cruds import movies_crud, users_crud
from app.utils.token import verify_token

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/{session_id}", response_class=HTMLResponse)
def session_detail(request: Request, session_id: int, db: Session = Depends(get_db)):
    # Проверяем токен пользователя
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login", status_code=303)

    try:
        username = verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login", status_code=303)

    # Получаем пользователя
    user = users_crud.get_user_by_username(db, username)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)

    # Получаем сеанс
    session = movies_crud.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Проверяем, есть ли уже бронирование на этот сеанс
    existing_booking = (
        db.query(BookingSession)
        .filter(BookingSession.user_id == user.id, BookingSession.movie_id == session.id)
        .first()
    )
    if existing_booking:
        # Если есть бронь, редиректим на профиль
        return RedirectResponse(url=f"/user/profile/session/{session_id}", status_code=303)

    # Если брони нет, отображаем страницу с деталями сеанса
    return templates.TemplateResponse("movie_detail_home.html", {"request": request, "session": session})
