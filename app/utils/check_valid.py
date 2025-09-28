from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.cruds import users_crud
from app.database.models import UserSession
from app.utils.token import verify_token


def check_token(request: Request, mode: bool = False) -> str | RedirectResponse:
    """
    Проверяет наличие и валидность токена в куках запроса.
    В зависимости от режима (user/admin) выбирает соответствующий токен и URL для редиректа.
    Если токен отсутствует или недействителен, возвращает RedirectResponse.
    Иначе возвращает проверенный токен.
    """
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
    """
    Проверяет существование пользователя в базе по username.
    Если пользователь не найден, возвращает RedirectResponse на страницу входа.
    Иначе возвращает объект UserSession с данными пользователя.
    """
    user = users_crud.get_user_by_username(db, username)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)
    return user
