from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    edad: int = Field(..., gt=60)
    historial_clinico: str = Field(...)
    estado: str = Field(...)
    proveedor_monetario: str = Field(...)
    saldo_mes: float = Field(..., gt=25.50)


class CrearCliente(ClienteBase):
    pass


class ActualizarCliente(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    edad:  Optional[int] = Field(None, gt=60)
    historial_clinico: Optional[str] = Field(None)
    estado: Optional[str] = Field(None)
    proveedor_monetario: Optional[str] = Field(None)
    saldo_mes: Optional[float] = Field(None, gt=25.50)


class ResidenteRespuesta(ClienteBase):
    id: int
    captado_el: datetime
    actualizado_el: Optional[datetime]
