from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.endpoints import orders, artworks, artists, admin, auth, webhook, seed, artworks_admin, artists_admin, create_admin, health, factura

app = FastAPI(title="Art Marketplace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(artists.router, prefix="/api/v1")
app.include_router(artworks.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(webhook.router, prefix="/api/v1")
app.include_router(seed.router, prefix="/api/v1")
app.include_router(artworks_admin.router, prefix="/api/v1")
app.include_router(artists_admin.router, prefix="/api/v1")
app.include_router(create_admin.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(factura.router, prefix="/api/v1")
