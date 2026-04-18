from fastapi import FastAPI
from .routers.sistem import router as sistem_router
from .routers.items import router as items_router
from .database.session import engine
from .models import item

item.Base.metadata.create_all(bind=engine)


model_tags = [
    {"name": "Items"},
    {"name": "Sistem"}
]

app = FastAPI(title="API de ventas de productos",
              version="1.0.0",
              openapi_tags=model_tags)

app.include_router(router=sistem_router, tags=["Sistem"])
app.include_router(router=items_router, tags=["Items"])
