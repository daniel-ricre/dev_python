from pydantic import BaseModel
from typing import Optional

# Esquema base compartido


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: Optional[str] = None
    imagen: Optional[str] = None

# Para crear un producto (se hereda todo)


class ProductoCreate(ProductoBase):
    pass

# Para la respuesta (incluye id)


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        orm_mode = True   # Permite que FastAPI convierta objetos SQLAlchemy a este esquema
