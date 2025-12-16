import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.repositories.user_repository import UserRepository
from app.models import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """СИНХРОННАЯ фикстура с async контекстом"""
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Запускаем event loop вручную
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def setup():
        async with async_session() as session:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            yield session
            await session.rollback()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

    session = loop.run_until_complete(setup())
    yield session
    loop.close()


@pytest.fixture(scope="function")
def user_repository(db_session):
    """UserRepository с тестовой БД"""
    loop = asyncio.get_event_loop()
    repo = UserRepository(db_session)
    yield repo
