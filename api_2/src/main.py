from fastapi import FastAPI
from .routers.users import router as users_router
from .database.session import Base, engine
from .routers.sistem import router as sistem_router

Base.metadata.create_all(bind=engine)

model_tags = [
    {"name": "Users"},
    {"name": "Sistem"},

]

app = FastAPI(title="Users Management API",
              version="1.0.0",
              openapi_tags=model_tags)


app.include_router(router=users_router, tags=["Users"])
app.include_router(router=sistem_router, tags=["Sistem"])
