from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, username: str) -> User:
        """Создаёт нового пользователя"""
        user = User(email=email, username=username)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Находит пользователя по email"""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(self, user_id: UUID, **data) -> Optional[User]:
        """Обновляет пользователя по ID"""
        user = await self.session.get(User, user_id)
        if user:
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

    async def delete(self, user_id: UUID) -> bool:
        """Удаляет пользователя по ID"""
        user = await self.session.get(User, user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Возвращает список пользователей с пагинацией"""
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
