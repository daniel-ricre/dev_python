from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.user import User
from app.core.security import get_password_hash
import uuid

router = APIRouter()

@router.post("/create-admin")
async def create_admin(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == "admin"))
    existing = result.scalar_one_or_none()
    if existing:
        return {"message": "El usuario admin ya existe", "username": "admin", "password": "admin123"}
    
    admin = User(
        id=uuid.uuid4(),
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_ong_admin=True
    )
    db.add(admin)
    await db.commit()
    return {"message": "Admin creado exitosamente", "username": "admin", "password": "admin123"}
