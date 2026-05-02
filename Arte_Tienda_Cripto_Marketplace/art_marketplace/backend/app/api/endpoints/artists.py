from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.artist import Artist

router = APIRouter()


@router.get("/artists")
async def list_artists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Artist))
    return result.scalars().all()
