from sqlalchemy.orm import Session
from ..models.worker import Trabajador
from ..schemas.workers import CrearTrabajador, AtualizarTrabajador
from fastapi import HTTPException, status


def crear_trabajador(db: Session, trabajador: CrearTrabajador):
    nuevo_trabajador = Trabajador(
        nombre=trabajador.nombre,
        edad=trabajador.edad,
        salario_mes=trabajador.salario_mes
    )
    db.add(nuevo_trabajador)
    db.commit()
    db.refresh(nuevo_trabajador)
    return nuevo_trabajador


def eliminar_trabajador(db: Session, trabajador_id: int):
    trabajador_encontrado = db.query(Trabajador).filter(
        Trabajador.id == trabajador_id).first()
    if not trabajador_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajador no encontrado"
        )
    db.delete(trabajador_encontrado)
    db.commit()
    return {"Mensaje": "Trabajador eliminado correctamente"}


def ver_trabajadores(db: Session, skip: int = 0, limit: int = 100):
    trabajadores = db.query(Trabajador).offset(skip).limit(limit).all()
    return trabajadores
