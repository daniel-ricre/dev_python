from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.deps import get_db

router = APIRouter()

@router.post("/migrate")
async def migrate_amount_column(db: AsyncSession = Depends(get_db)):
    """Endpoint temporal para cambiar amount de BIGINT a NUMERIC."""
    await db.execute(text("ALTER TABLE orders ALTER COLUMN amount TYPE NUMERIC"))
    await db.commit()
    return {"message": "Migración completada: amount ahora es NUMERIC"}
