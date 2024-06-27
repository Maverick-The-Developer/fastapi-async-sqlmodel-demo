from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncIterator

DATABASE_URL = "sqlite+aiosqlite:///./sqlite-data.db"

engine = create_async_engine(DATABASE_URL, echo=True)

sessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def init_db():
    print("##### Initializing database #####")
    async with engine.begin() as conn:
        print("===== Creating tables ======")
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with sessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
