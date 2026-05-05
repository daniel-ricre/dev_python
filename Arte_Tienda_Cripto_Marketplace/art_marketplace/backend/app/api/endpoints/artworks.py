from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import get_db
from app.models.artwork import Artwork
import uuid

router = APIRouter()


@router.get("/artworks")
async def list_artworks(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Artwork)
        .where(Artwork.available == True)
        .options(joinedload(Artwork.artist))
    )
    result = await db.execute(stmt)
    return result.unique().scalars().all()


@router.get("/artworks/{artwork_id}")
async def get_artwork(
    artwork_id: str = Path(..., description="UUID de la obra"),
    db: AsyncSession = Depends(get_db)
):
    # Validar que el ID sea un UUID válido
    try:
        uuid.UUID(artwork_id)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"ID inválido: '{artwork_id}' no es un UUID válido. Debe tener formato como '550e8400-e29b-41d4-a716-446655440000'"
        )
    
    stmt = (
        select(Artwork)
        .where(Artwork.id == artwork_id)
        .options(joinedload(Artwork.artist))
    )
    result = await db.execute(stmt)
    artwork = result.unique().scalar_one_or_none()
    if not artwork:
        raise HTTPException(status_code=404, detail=f"Obra con ID '{artwork_id}' no encontrada")
    return artwork
