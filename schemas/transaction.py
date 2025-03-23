import os

from pydantic import BaseModel

from utils import hash_string


class TransactionBase(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float | int


class TransactionResponse(TransactionBase):
    signature: str

    def validate_signature(self, payment_key: str):
        return self.signature == hash_string(self.concatenated_string(payment_key))

    def concatenated_string(self, payment_key: str) -> str:
        concatenated_string = f"{self.account_id}{self.amount}{self.transaction_id}{self.user_id}{payment_key}"
        return concatenated_string


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True
