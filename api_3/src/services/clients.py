from sqlalchemy.orm import Session
from ..schemas.clients import CrearCliente, ActualizarCliente, ResidenteRespuesta
from ..models.client import Residente
from fastapi import HTTPException, status


def crear_cliente(db: Session, cliente: CrearCliente):
    nuevo_cliente = Residente(
        nombre=cliente.nombre,
        edad=cliente.edad,
        historial_clinico=cliente.historial_clinico,
        estado=cliente.estado,
        proveedor_monetario=cliente.proveedor_monetario,
        saldo_mes=cliente.saldo_mes
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


def eliminar_cliente(db: Session, cliente_id: int):
    cliente_encontrado = db.query(Residente).filter(
        Residente.id == cliente_id).first()
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    db.delete(cliente_encontrado)
    db.commit()
    return {"Mensaje": "Cliente eliminado correctamente"}


def ver_clientes(db: Session, skip: int = 0, limit: int = 100):
    clientes = db.query(Residente).offset(skip).limit(limit).all()
    return clientes
