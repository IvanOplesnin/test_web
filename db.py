import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

pg_link = os.getenv("PG_LINK")

engine = create_async_engine(pg_link, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
