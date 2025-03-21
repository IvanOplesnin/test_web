from pydantic import BaseModel


class TransactionBase(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True
