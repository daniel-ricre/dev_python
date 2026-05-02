from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from ..database.session import Base


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    edad = Column(Integer, nullable=False)
    salario_mes = Column(Float, index=True, nullable=False)

    contratado_el = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_el = Column(DateTime(timezone=True), onupdate=func.now())
