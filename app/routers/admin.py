from fastapi import Request, HTTPException, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.orm import Session
from starlette.templating import _TemplateResponse

from app.schemas import MovieSessionForm
from app.config import ADMINS
from app.token import create_token, verify_token
from app.database.session import get_db
from app.database import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SESSIONS = []


@router.get("/login", response_class=HTMLResponse)
def login_admin_get(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login")
async def login(
        username: Annotated[str, Form(..., description="Admin username")],
        password: Annotated[str, Form(..., description="Admin password")]
) -> RedirectResponse:
    if username in ADMINS and ADMINS[username] == password:
        token = create_token(username)
        response = RedirectResponse(url="/admin/panel", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid username or password")


@router.get("/panel")
async def panel(request: Request, db: Session = Depends(get_db)) -> _TemplateResponse:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token)

    sessions = crud.get_sessions(db)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "sessions": sessions})


@router.get("/logout", response_class=RedirectResponse)
async def logout() -> RedirectResponse:
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.post("/add-session")
async def add_session(
        request: Request,
        movie: str = Form(...),
        time: str = Form(...),
        hall: str = Form(...),
        seats: int = Form(...),
        db: Session = Depends(get_db)
) -> RedirectResponse:
    # Проверяем токен
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token)

    # Создаём Pydantic объект
    session = MovieSessionForm(movie=movie, time=time, hall=hall, seats=seats)
    crud.create_session(db, session)

    # Редирект обратно на панель
    response = RedirectResponse(url="/admin/panel", status_code=303)
    return response


@router.post("/delete-session/{session_id}")
async def delete_session(session_id: int, request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    # Проверяем токен администратора
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token)

    # Удаляем сеанс через CRUD
    session_to_delete = crud.get_session_by_id(db, session_id)
    if not session_to_delete:
        raise HTTPException(status_code=404, detail="Session not found")

    crud.delete_session(db, session_id)

    return RedirectResponse(url="/admin/panel", status_code=303)
