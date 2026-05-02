from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    is_active: Optional[bool]


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
