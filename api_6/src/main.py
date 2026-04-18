from fastapi import FastAPI

from .routers import router_admin
from .routers import user_router
from .database.session import engine, Base
from .models import user_models

Base.metadata.create_all(bind=engine)

model_tags = [
    {"name": "Sistem"},
    {"name": "Users"},
    {"name": "Admin"},
]

app = FastAPI(
    title="User Management API",
    description="Production-ready REST API for user management with authentication, admin control, and secure password handling.",
    version="1.0.0",
    openapi_tags=model_tags
)

app.include_router(prefix="/router", router=user_router.router, tags=["Users"])
app.include_router(
    prefix="/router", router=router_admin.router, tags=["Admin"])


@app.get("/", tags=["Sistem"])
def get_root():
    return {"Message": "Welcome to 'API test'"}


@app.head("/", tags=["Sistem"])
def get_health():
    return
