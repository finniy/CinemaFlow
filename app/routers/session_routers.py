from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.session import get_db
from app.database.cruds import movies_crud
from app.utils.token import verify_token

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/{session_id}", response_class=HTMLResponse)
def session_detail(request: Request, session_id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token_user")
    if not token:
        return RedirectResponse(url="/user/login")

    try:
        verify_token(token, mode=False)
    except Exception:
        return RedirectResponse(url="/user/login")

    session = movies_crud.get_session_by_id(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return templates.TemplateResponse("movie_detail_home.html", {"request": request, "session": session})
