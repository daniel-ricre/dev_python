from pydantic import BaseModel, ConfigDict
from typing import Optional


class DateBase(BaseModel):
    year: str
    mont: str
    day: str
    aviable: str
    unaviable: Optional[str]


class DateCreate(DateBase):
    pass


class DateUpdate(BaseModel):
    year: Optional[str]
    mont: Optional[str]
    day: Optional[str]
    aviable: Optional[str]
    unavible: Optional[str]


class DateResponse(DateBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
