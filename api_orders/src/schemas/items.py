from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemBase(BaseModel):
    name: str
    price: float
    stock: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    stock: Optional[int]


class ItemResponse(ItemBase):

    model_config = ConfigDict(from_attributes=True)
