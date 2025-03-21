from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    user_id: int = Field(...)
    balance: float = Field(...)


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int = Field(...)

    class Config:
        from_attributes = True



