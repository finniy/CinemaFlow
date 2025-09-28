from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.cruds import movies_crud
from app.utils.token import verify_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home_get(request: Request, db: Session = Depends(get_db)):
    """
    Отображает главную страницу пользователя с предстоящими сеансами фильмов.
    Проверяет наличие и валидность токена пользователя в cookie.
    Если токен отсутствует или недействителен, делает редирект на страницу входа.
    Получает все сеансы с базовыми данными и передает их в шаблон 'home.html'.
    """
    # Проверяем токен пользователя
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login")

    try:
        verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login")

    sessions_full = movies_crud.get_sessions(db, mode=True)

    # Создаём список только с базовыми полями
    sessions = [
        {
            "id": s.id,
            "movie": s.movie,
            "cinema": s.cinema,
            "time": s.time
        }
        for s in sessions_full
    ]

    return templates.TemplateResponse("home.html", {"request": request, "sessions": sessions})
