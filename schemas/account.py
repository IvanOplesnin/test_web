from typing import Optional

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    id: Optional[int] = Field(None, alias="account_id")
    user_id: int = Field(...)
    balance: float = 0.0


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int = Field(...)

    class Config:
        from_attributes = True



