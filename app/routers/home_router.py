from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.utils.token import verify_token
from app.database.session import get_db
from app.database.cruds import movies_crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home_get(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login")

    try:
        verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login")

    sessions = movies_crud.get_sessions(db, mode=True)
    return templates.TemplateResponse("home.html", {"request": request, "sessions": sessions})
