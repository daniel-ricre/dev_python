from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.session import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True, nullable=False)
    color = Column(String, index=True, nullable=False)
    # serie = Column(String, unique=True, index=True, nullable=False)
    # propietary = Column(String, index=True, nullable=False)
    cost = Column(Float, index=True, nullable=False)
    # status = Column(Float, index=True, nullable=False)
    # work_cost = Column(Float, index=True, nullable=False)
    # aproximatly_time_to_work = Column(String, index=True, nullable=False)
    # plate = Column(String, index=True, nullable=False)

    mechanic = relationship(foreign_keys="id", back_populates="cars.id")
