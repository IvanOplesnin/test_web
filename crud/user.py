from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User
from schemas import UserCreate
from utils import hash_password


async def select_user(*, user_id: int,
                      session: AsyncSession):
    stmt = (select(User).
            where(User.id == user_id).
            options(selectinload(User.accounts), selectinload(User.transactions)))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def select_user_by_email(*, email: str, session: AsyncSession) -> User:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        return user


async def get_all_users(*, session: AsyncSession) -> list[User]:
    stmt = select(User).options(selectinload(User.accounts), selectinload(User.transactions))
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_user(*, user: UserCreate, session: AsyncSession) -> User:
    user = user.model_dump()
    user["hash_password"] = hash_password(user.pop("password"))
    user = User(**user)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


if __name__ == "__main__":
    from db import async_session
    import asyncio


    async def main():
        async with async_session() as session:
            new_user = await select_user_by_email(email="admin@example.com", session=session)
            print(new_user.id)


    asyncio.run(main())
