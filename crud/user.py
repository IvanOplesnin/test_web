from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User
from schemas import UserCreate, UserUpdate
from utils import hash_string


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


async def user_add(*, user: UserCreate, session: AsyncSession) -> User:
    new_user = user.model_dump()
    new_user["hash_password"] = hash_string(new_user.pop("password"))
    new_user = User(**new_user)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def user_update(*, user_id: int, user: UserUpdate, session: AsyncSession) -> User:
    user_model = user.model_dump(exclude_none=True)
    if user_model.get("password"):
        user_model["hash_password"] = hash_string(user_model.pop("password"))
    stmt = update(User).where(User.id == user_id).values(user_model).returning(User)

    new_user = await session.execute(stmt)
    await session.commit()

    return new_user


async def user_delete(*, user_id: int, session: AsyncSession) -> User:
    stmt = delete(User).where(User.id == user_id)

    await session.execute(stmt)
    await session.commit()




if __name__ == "__main__":
    pass
