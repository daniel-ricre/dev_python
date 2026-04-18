from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=2,
                          max_length=20, examples=["Jhon Die"])
    password: str = Field(..., min_length=6, examples=["pass123"])
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=2, max_length=20, examples=["Jhony Dutte"])
    password: Optional[str] = Field(
        None, min_length=6, examples=["newpass123"])
    email: Optional[EmailStr]


class UserResponse(UserBase):
    pass


class UserResponseAdmin(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
