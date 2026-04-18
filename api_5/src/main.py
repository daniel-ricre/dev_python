from fastapi import FastAPI
from .database.session import Base, engine
from .routers.dates import router as router_date

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=router_date, tags=["Gestion"])
