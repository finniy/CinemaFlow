from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def register_exception_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code in (400, 401, 403, 404, 405, 409, 422, 500, 503):
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "status_code": exc.status_code},
                status_code=exc.status_code
            )
        # остальные ошибки — пробрасываем дальше
        raise exc
