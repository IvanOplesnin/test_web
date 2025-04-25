import os
from typing import Optional

from pydantic import BaseModel, Field

from utils import hash_string


class TransactionBase(BaseModel):
    transaction_id: str
    user_id: int
    account_id: Optional[int] = Field(None)
    amount: float | int


class TransactionResponse(TransactionBase):
    signature: str

    def validate_signature(self, payment_key: str):
        return self.signature == hash_string(self.concatenated_string(payment_key))

    def concatenated_string(self, payment_key: str) -> str:
        account_id = self.account_id
        if not self.account_id:
            account_id = 'null'
        concatenated_string = f"{account_id}{self.amount}{self.transaction_id}{self.user_id}{payment_key}"
        return concatenated_string


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True


