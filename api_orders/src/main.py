from fastapi import FastAPI
from .database.session import engine, Base
from .routers.clients import router as router_clients
from .routers.worker import router as router_worker
from .routers.sistem import router as router_sistem

Base.metadata.create_all(bind=engine)

model_tags = [
    {"name": "Clients"},
    {"name": "Worker"},
    {"name": "Sistem"}
]

app = FastAPI(title="El Tornillo Feliz",
              description="API for product managment to Don Manuel",
              version="1.0.0",
              openapi_tags=model_tags)

app.include_router(router=router_clients, tags=["Clients"])
app.include_router(router=router_worker, tags=["Worker"])
app.include_router(router=router_sistem, tags=["Sistem"])
