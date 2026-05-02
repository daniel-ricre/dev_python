from sqlalchemy import Column, String, Float, Integer
from ..database.session import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    price = Column(Float, index=True)
    stock = Column(Integer)
