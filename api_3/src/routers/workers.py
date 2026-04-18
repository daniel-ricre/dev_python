from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..schemas.workers import CrearTrabajador, RespuestaTrabajador, AtualizarTrabajador
from ..services import workers


router = APIRouter(prefix="/trabajadores")


@router.post("/nuevo_trabajador", response_model=RespuestaTrabajador, status_code=status.HTTP_201_CREATED)
def nuevo_trabajador(trabajador: CrearTrabajador, db: Session = Depends(get_db)):
    return workers.crear_trabajador(db, trabajador)


@router.get("/ver_trabajadores", response_model=List[RespuestaTrabajador])
def ver_trabajadores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return workers.ver_trabajadores(db, skip, limit)


@router.delete("/eliminar_trabajador")
def eliminar_trabajador(trabajador_id: int, db: Session = Depends(get_db)):
    return workers.eliminar_trabajador(db, trabajador_id)
