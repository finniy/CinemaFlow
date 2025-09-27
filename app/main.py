from fastapi import FastAPI
from app.routers import admin
from uvicorn import run

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["admin"])

if __name__ == '__main__':
    run('main:app', host='127.0.0.1', port=8000)
