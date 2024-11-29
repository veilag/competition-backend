from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
