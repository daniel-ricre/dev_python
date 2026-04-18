from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from ..database.session import Base


class DateT(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String, index=True)
    mont = Column(String, index=True)
    day = Column(String, index=True)
    aviable = Column(String, index=True)
    unaviable = Column(String, index=True)
