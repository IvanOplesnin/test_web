from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User
from app.schemas.user import UserCreate
from app.utils import hash_password


async def select_user(*, user_id: int,
                      session: AsyncSession):
    stmt = (select(User).
            where(User.id == user_id).
            options(selectinload(User.accounts), selectinload(User.transactions)))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def all_users(*, session: AsyncSession) -> list[User]:
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
    from app.db import async_session
    import asyncio


    async def main():
        async with async_session() as session:
            user = {
                "fullname": "Оплеснин Иван",
                "email": "ivan@example.com",
                "password": "ivan123",
                "is_admin": True
            }
            new_user = UserCreate(**user)
            await create_user(user=new_user, session=session)


    asyncio.run(main())
