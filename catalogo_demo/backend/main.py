from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database.session import engine, Base
from routers import clients, admin

# Crear todas las tablas automáticamente al iniciar (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catálogo Mipime - SQLite",
    description="API con base de datos SQLite y separación modular",
    version="2.0.0"
)

# CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(clients.router)
app.include_router(admin.router)

# (Opcional) Servir el frontend estático (cuando quieras integrar todo)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Punto de entrada para desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
