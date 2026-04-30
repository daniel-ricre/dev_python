from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import SessionLocal
from schemas.product import ProductoCreate, ProductoResponse
from services.product import crear_producto, eliminar_producto

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/productos", response_model=ProductoResponse, status_code=201)
def crear_producto_endpoint(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, producto)


@router.delete("/productos/{producto_id}", response_model=ProductoResponse)
def eliminar_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    producto = eliminar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto
