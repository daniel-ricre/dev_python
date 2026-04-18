from fastapi import APIRouter, Depends, status
from ..services import clients
from ..schemas.clients import ResidenteRespuesta, CrearCliente
from sqlalchemy.orm import Session
from ..database.session import get_db
from typing import List


router = APIRouter(prefix="/Residentes")


@router.post("/nuevo_residente", response_model=ResidenteRespuesta, status_code=status.HTTP_201_CREATED)
def nuevo_residente(residente: CrearCliente, db: Session = Depends(get_db)):
    return clients.crear_cliente(db, residente)


@router.get("/ver_residente", response_model=List[ResidenteRespuesta])
def ver_residente(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return clients.ver_clientes(db, skip, limit)


@router.delete("/eliminar_residente")
def eliminar_residente(residente_id: int, db: Session = Depends(get_db)):
    return clients.eliminar_cliente(db, residente_id)
