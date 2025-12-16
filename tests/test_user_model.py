import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models import User, Base


@pytest.mark.asyncio
async def test_create_user_model():
    """Тест модели User — создание + SQL логи"""
    engine = create_async_engine("sqlite+aiosqlite:///./test_model.db", echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Создаём User напрямую
        user = User(username="john_doe", email="test@example.com", description="test user")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Проверяем модель
        assert user.id is not None
        assert user.username == "john_doe"
        assert user.email == "test@example.com"
        print(f"✅ User ID: {user.id}")

    await engine.dispose()
