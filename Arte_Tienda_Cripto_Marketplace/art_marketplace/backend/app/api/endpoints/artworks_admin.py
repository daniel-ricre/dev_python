from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from app.api.deps import get_current_ong_admin, get_db
from app.models.artwork import Artwork
from app.models.artist import Artist
import uuid

router = APIRouter()

class ArtworkCreate(BaseModel):
    title: str = Field(..., description="Titulo de la obra")
    description: str = Field("", description="Descripcion")
    price_usd: float = Field(..., gt=0, description="Precio en USD")
    image_url: str = Field(..., description="URL de la imagen")
    artist_id: str = Field(..., description="UUID del artista")
    available: bool = Field(default=True)

@router.post("/admin/artworks")
async def create_artwork(
    data: ArtworkCreate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_ong_admin)
):
    result = await db.execute(select(Artist).where(Artist.id == data.artist_id))
    artist = result.scalar_one_or_none()
    if not artist:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    
    artwork = Artwork(
        id=uuid.uuid4(),
        title=data.title,
        description=data.description,
        price_usd=data.price_usd,
        image_url=data.image_url,
        artist_id=data.artist_id,
        available=data.available
    )
    db.add(artwork)
    await db.commit()
    await db.refresh(artwork)
    return artwork
