from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database.session import SessionLocal
from schemas.product import ProductoResponse
from services.product import obtener_productos, obtener_producto_por_id

router = APIRouter(
    prefix="/api",
    tags=["clientes"]
)

# Dependencia para obtener la sesión de DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/productos", response_model=List[ProductoResponse])
def listar_productos(
    categoria: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    productos = obtener_productos(db, categoria=categoria)
    return productos


@router.get("/productos/{producto_id}", response_model=ProductoResponse)
def ver_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = obtener_producto_por_id(db, producto_id)
    if not producto:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto
