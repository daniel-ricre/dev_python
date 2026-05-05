# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# ⭐ CONFIGURACIÓN CORS - Agrega esto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tus dominios
    allow_credentials=True,
    # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(router=users_router, tags=["Users"])
app.include_router(router=sistem_router, tags=["Sistem"])
