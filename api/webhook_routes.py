import os

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from crud import transaction_add
from db import get_session
from schemas import TransactionResponse, TransactionRead

webhook_router = APIRouter(prefix='/webhook')


@webhook_router.post('/payment', response_model=TransactionRead)
async def payment_webhook(response: TransactionResponse, session=Depends(get_session)):
    payment_key = os.getenv('PAYMENT_KEY')

    if response.validate_signature(payment_key):
        transaction = await transaction_add(response=response, session=session)
        return transaction

    raise HTTPException(status_code=403, detail='Invalid signature')





