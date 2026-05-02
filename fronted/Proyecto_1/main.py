from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database.session import Base, engine, get_db
from .routers.users import router as users_router
from .routers.admin import router as admin_router
from .routers.sistem import router as sistem_router
from .services.users import create as create_user_service
from .schemas.users import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=users_router, tags=["Users"])
app.include_router(router=admin_router, tags=["Admin"])
app.include_router(router=sistem_router, tags=["Sistem"])
