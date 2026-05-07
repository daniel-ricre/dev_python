from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.api.deps import get_current_ong_admin, get_db
from app.models.artist import Artist
import uuid

router = APIRouter()

class ArtistCreate(BaseModel):
    name: str = Field(..., description="Nombre del artista")
    bio: str = Field("", description="Biografia")
    wallet_address: str = Field(..., description="Direccion de wallet Ethereum")
    image_url: str = Field("", description="URL de la imagen de perfil")

@router.post("/admin/artists")
async def create_artist(
    data: ArtistCreate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_ong_admin)
):
    artist = Artist(
        id=uuid.uuid4(),
        name=data.name,
        bio=data.bio,
        wallet_address=data.wallet_address,
        image_url=data.image_url
    )
    db.add(artist)
    await db.commit()
    await db.refresh(artist)
    return artist
