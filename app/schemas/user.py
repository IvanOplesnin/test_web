from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    fullname: str = Field(..., min_length=4)
    email: EmailStr = Field(...)
    is_admin: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(UserBase):
    fullname: Optional[str] = Field(None, min_length=4)
    email: Optional[str] = Field(None)
    is_admin: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
