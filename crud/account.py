from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Account
from schemas import AccountCreate, TransactionResponse


async def create_account(*, account: AccountCreate, session: AsyncSession) -> Account:
    acc = await get_account_by_id(account.id, session)
    if acc is not None:
        raise ValueError('This account already exists')

    acc_dict = account.model_dump()
    acc_dict.pop('id')
    new_account = Account(**acc_dict)
    session.add(new_account)

    await session.commit()
    await session.refresh(new_account)

    return new_account


async def update_balance(transaction: TransactionResponse, session: AsyncSession) -> Account:
    acc = await get_account_by_id(transaction.account_id, session)
    new_balance = acc.balance + transaction.amount
    stmt = (update(Account).where(Account.id == transaction.account_id).
            values(balance=new_balance).
            returning(Account))

    account = await session.execute(stmt)
    await session.commit()

    return account.scalar_one_or_none()


async def get_accounts(account_id: int, session: AsyncSession) -> list[Account]:
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_account_by_id(account_id: int, session: AsyncSession) -> Account:
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
