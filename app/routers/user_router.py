from fastapi import Request, HTTPException, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.orm import Session
from starlette.templating import _TemplateResponse

from app.utils.security import verify_password, hash_password
from app.schemas import UserRegister
from app.utils.token import create_token
from app.database.session import get_db
from app.database.cruds import users_crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register_user_get(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register")
async def register_user_post(
        username: Annotated[str, Form(..., description="User login")],
        password: Annotated[str, Form(..., description="User password")],
        db: Session = Depends(get_db)
) -> RedirectResponse:
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
    return response


@router.get("/login", response_class=HTMLResponse)
async def register_user_get(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("user_login.html", {"request": request})


@router.post("/login")
async def login_user_post(
        username: Annotated[str, Form(..., description="User login")],
        password: Annotated[str, Form(..., description="User password")],
        db: Session = Depends(get_db)
) -> RedirectResponse:
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
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token_user")
    return response