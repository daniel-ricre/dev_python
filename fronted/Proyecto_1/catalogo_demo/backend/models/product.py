from sqlalchemy import Column, Integer, String, Float
from database.session import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    categoria = Column(String, nullable=True)
    imagen = Column(String, nullable=True)   # ruta relativa de la imagen
