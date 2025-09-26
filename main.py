from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run

from app.config import ADMINS
from app.token import create_token, verify_token

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/admin/login", response_class=HTMLResponse)
def login_admin_get(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/admin/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in ADMINS and ADMINS[username] == password:
        token = create_token(username)
        response = RedirectResponse(url="/admin/panel", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/admin/panel")
async def panel(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found")
    username = verify_token(token)
    return {"message": f"Welcome, {username}!"}


if __name__ == '__main__':
    run('main:app', host='127.0.0.1', port=8000)
