from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
import re

# Forzar el driver asyncpg independientemente de lo que venga en la URL
db_url = settings.DATABASE_URL
db_url = re.sub(r'^postgresql://', 'postgresql+asyncpg://', db_url)
db_url = re.sub(r'^postgres://', 'postgresql+asyncpg://', db_url)

Base = declarative_base()

engine = create_async_engine(db_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
