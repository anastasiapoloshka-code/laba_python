import os

# Импорты контроллера и сервисов (МИНИМАЛЬНЫЕ заглушки)
from controllers.user_controller import UserController
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ---------- Настройка базы данных ----------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./test.db",  # SQLite по умолчанию
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------- Провайдеры (МИНИМАЛЬНЫЕ заглушки) ----------
class MockUserRepository:
    async def get_all(self, count: int = 10, page: int = 1):
        return [], 0


class MockUserService:
    async def get_by_filter(self, count: int, page: int):
        return [], 0


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession):
    return MockUserRepository()


async def provide_user_service(user_repository):
    return MockUserService()


# ---------- Приложение ----------
app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
