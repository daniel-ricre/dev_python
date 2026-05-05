from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=2, examples=["Anthony"])
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, examples=["my456n"])


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=2, examples=["Anthon"])
    email: Optional[EmailStr]
    password: Optional[str] = Field(
        None, min_length=6, examples=["new123"])
    is_active: Optional[bool]


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
