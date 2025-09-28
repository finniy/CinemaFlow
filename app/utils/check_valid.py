from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.cruds import users_crud
from app.utils.token import verify_token
from app.database.models import UserSession


def check_token(request: Request, mode: bool = False) -> str | RedirectResponse:
    redirect_url = "/user/login" if not mode else "/admin/login"
    cookie_name = "access_token_user" if not mode else "access_token_admin"

    token = request.cookies.get(cookie_name)
    if not token:
        return RedirectResponse(url=redirect_url, status_code=303)

    try:
        return verify_token(token, mode=mode)
    except Exception:
        return RedirectResponse(url=redirect_url, status_code=303)


def check_user(db: Session, username: str) -> UserSession | RedirectResponse:
    user = users_crud.get_user_by_username(db, username)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)
    return user
