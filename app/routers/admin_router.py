from fastapi import Request, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.orm import Session
from starlette.templating import _TemplateResponse
from datetime import datetime

from app.utils.check_valid import check_user, check_token
from app.utils.security import verify_password
from app.utils.schemas import MovieSessionFull
from app.config import ADMINS
from app.utils.token import create_token, verify_token
from app.database.session import get_db
from app.database.cruds import movies_crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_admin_get(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login")
async def login_admin_post(
        username: Annotated[str, Form(..., description="Admin username")],
        password: Annotated[str, Form(..., description="Admin password")]
) -> RedirectResponse:
    if username in ADMINS and verify_password(password, ADMINS[username]):
        token = create_token(username, mode=True)
        response = RedirectResponse(url="/admin/panel", status_code=303)
        response.set_cookie(key="access_token_admin", value=token, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid username or password")


from fastapi import HTTPException


@router.get("/panel")
async def panel_admin_get(request: Request, db: Session = Depends(get_db)):
    # Проверяем токен и получаем username
    username_or_redirect = check_token(request, mode=True)
    if isinstance(username_or_redirect, RedirectResponse):
        return username_or_redirect

    sessions = movies_crud.get_sessions(db)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "sessions": sessions})


@router.get("/logout", response_class=RedirectResponse)
async def logout_admin_get() -> RedirectResponse:
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token_admin")
    return response


@router.post("/add-session")
async def add_session_post(
        request: Request,
        movie: str = Form(...),
        cinema: str = Form(...),
        date: str = Form(...),
        time: str = Form(...),
        hall: str = Form(...),
        seats: int = Form(...),
        duration: int = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db)
) -> RedirectResponse:
    # Проверяем токен
    token = request.cookies.get("access_token_admin")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token, mode=True)

    # Парсим дату и время
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    # Создаём Pydantic объект
    session = MovieSessionFull(
        movie=movie,
        cinema=cinema,
        time=dt,
        hall=hall,
        seats=seats,
        duration=duration,
        description=description
    )

    # Сохраняем в БД
    movies_crud.create_session(db, session)

    # Редирект обратно на панель
    response = RedirectResponse(url="/admin/panel", status_code=303)
    return response


@router.post("/delete-session/{session_id}")
async def delete_session_post(session_id: int, request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    # Проверяем токен администратора
    token = request.cookies.get("access_token_admin")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token, mode=True)

    # Удаляем сеанс через CRUD
    session_to_delete = movies_crud.get_session_by_id(db, session_id)
    if not session_to_delete:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        movies_crud.delete_session(db, session_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Session not deleted")

    return RedirectResponse(url="/admin/panel", status_code=303)
