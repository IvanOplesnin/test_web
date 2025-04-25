

import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from crud import create_account
from crud.account import get_account_by_id, update_balance
from models import Transaction
from schemas import TransactionResponse, AccountCreate


async def transaction_add(*, response: TransactionResponse, session: AsyncSession):
    new_acc = await create_account_if_exist(response=response, session=session)

    dict_response = response.model_dump()
    del dict_response['signature']
    new_transaction = Transaction(**dict_response)
    if new_acc:
        new_transaction.account_id = new_acc.id
    try:
        session.add(new_transaction)
        await update_balance(transaction=new_transaction, session=session)
        await session.commit()
        await session.refresh(new_transaction)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail='The money has already been credited')

    return new_transaction


async def create_account_if_exist(*, response: TransactionResponse, session: AsyncSession):
    account = None
    if response.account_id:
        account = await get_account_by_id(account_id=response.account_id, session=session)
    if not account:
        print(f'---------------{response.account_id}------------------------')
        acc = AccountCreate(user_id=response.user_id, account_id=response.account_id)
        new_acc = await create_account(account=acc, session=session)
        return new_acc
