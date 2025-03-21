from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Account
from app.schemas.account import AccountCreate
from app.utils import hash_password


async def create_account(*, account: AccountCreate, session: AsyncSession) -> Account:
    new_account = Account(**account.model_dump())
    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)
    return new_account


async def get_accounts(user_id: int, session: AsyncSession) -> list[Account]:
    stmt = select(Account).where(Account.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()