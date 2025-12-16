@pytest.mark.asyncio
async def test_create_user_simple():
    """Простой тест без фикстур"""
    from app.models import User, Base
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from app.repositories.user_repository import UserRepository

    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        repo = UserRepository(session)
        user = await repo.create(email="test@example.com", username="john_doe")
        assert user.id is not None
        assert user.email == "test@example.com"

    await engine.dispose()
