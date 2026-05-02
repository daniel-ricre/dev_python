from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import get_db
from app.models.artwork import Artwork

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
async def get_artwork(artwork_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Artwork)
        .where(Artwork.id == artwork_id)
        .options(joinedload(Artwork.artist))
    )
    result = await db.execute(stmt)
    artwork = result.unique().scalar_one_or_none()
    if not artwork:
        raise HTTPException(status_code=404)
    return artwork
