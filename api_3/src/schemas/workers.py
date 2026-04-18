from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TrabajadorBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    edad: int = Field(..., gt=18)
    salario_mes: float = Field(..., gt=5000)


class CrearTrabajador(TrabajadorBase):
    pass


class AtualizarTrabajador(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    edad: Optional[int] = Field(None, gt=18)
    salario_mes: Optional[float] = Field(None, gt=5000)


class RespuestaTrabajador(TrabajadorBase):
    id: int
    contratado_el: datetime
    actualizado_el: Optional[datetime]
