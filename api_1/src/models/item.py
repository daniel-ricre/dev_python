from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, Float
from sqlalchemy.sql import func
from ..database.session import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, index=True, nullable=False)

    is_aviable = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
