from fastapi import FastAPI
from .routers.clients import router as router_clientes
from .routers.workers import router as router_trabajadores
from .routers.sistem import router as router_sistema
from .database.session import Base, engine

Base.metadata.create_all(bind=engine)

model_tags = [
    {"nombre": "Trabajadores"},
    {"nombre": "Residentes"},
    {"nombre": "Sistema"}
]

app = FastAPI(title="API de gestion de Hogar de Ancianos")
app.include_router(router=router_clientes, tags=["Residentes"])
app.include_router(router=router_trabajadores, tags=["Trabajadores"])
app.include_router(router=router_sistema, tags=["Sistema"])
