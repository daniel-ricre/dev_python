from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., min_length=3, examples=["apple"])
    type: str = Field(..., min_length=3, examples=["fruit"])
    description: str = Field(..., examples=[
                             "A delicious fruit for eat in the morning"])
    price: float = Field(..., gt=0, examples=["1.25"])


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, examples=["apple"])
    type: Optional[str] = Field(None, min_length=3, examples=["fruit"])
    description: Optional[str] = Field(None, examples=[
                                       "A delicious fruit for eat in family"])
    price: Optional[float] = Field(None, gt=0, examples=["1.25"])
    is_aviable: Optional[bool]


class ItemResponse(ItemBase):
    id: int
    is_aviable: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
