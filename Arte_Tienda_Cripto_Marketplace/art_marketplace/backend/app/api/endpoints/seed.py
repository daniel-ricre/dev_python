from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.artist import Artist
from app.models.artwork import Artwork
import uuid

router = APIRouter()


@router.post("/seed")
async def seed_data(db: AsyncSession = Depends(get_db)):
    """Endpoint temporal para insertar datos de prueba."""
    artist_id = uuid.uuid4()
    artist = Artist(
        id=artist_id,
        name="Ana María López",
        bio="Artista cubana contemporánea",
        wallet_address="0x3aA0A7f39C6e2FCa0c4b3bC1c31eB1FBDa9D678e",
        image_url="https://via.placeholder.com/150"
    )
    db.add(artist)
    
    artwork_id = uuid.uuid4()
    artwork = Artwork(
        id=artwork_id,
        title="Atardecer en La Habana",
        description="Óleo sobre lienzo, 60x80 cm",
        price_usd=350.00,
        image_url="https://via.placeholder.com/400",
        artist_id=artist_id,
        available=True
    )
    db.add(artwork)
    
    await db.commit()
    
    return {
        "artist_id": str(artist_id),
        "artwork_id": str(artwork_id),
        "title": artwork.title,
        "price_usd": artwork.price_usd
    }
