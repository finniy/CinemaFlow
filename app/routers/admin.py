from fastapi import Request, HTTPException, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.orm import Session

from app.schemas import MovieSessionForm
from app.config import ADMINS
from app.token import create_token, verify_token
from app.database.session import get_db
from app.database import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SESSIONS = []


@router.get("/login", response_class=HTMLResponse)
def login_admin_get(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login")
async def login(
        username: Annotated[str, Form(..., description="Admin username")],
        password: Annotated[str, Form(..., description="Admin password")]
):
    if username in ADMINS and ADMINS[username] == password:
        token = create_token(username)
        response = RedirectResponse(url="/admin/panel", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid username or password")


@router.get("/panel")
async def panel(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    verify_token(token)

    sessions = crud.get_sessions(db)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "sessions": sessions})


@router.get("/logout", response_class=RedirectResponse)
async def logout():
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
):
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
