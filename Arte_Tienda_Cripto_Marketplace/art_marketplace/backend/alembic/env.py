# alembic/env.py (modificado)
from app.core.config import settings
from app.core.database import Base
from app.models import order, artwork, artist, user

target_metadata = Base.metadata

def get_url():
    return settings.DATABASE_URL.replace("asyncpg", "psycopg2")  # sync para migraciones