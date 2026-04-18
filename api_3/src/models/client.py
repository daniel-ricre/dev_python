from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from ..database.session import Base


class Residente(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    edad = Column(Integer, index=True, nullable=False)
    historial_clinico = Column(Text, nullable=False)
    estado = Column(String, nullable=False, index=True)
    proveedor_monetario = Column(String, nullable=False, index=True)
    saldo_mes = Column(Float, index=True, nullable=False)

    captado_el = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_el = Column(DateTime(timezone=True), onupdate=func.now())
