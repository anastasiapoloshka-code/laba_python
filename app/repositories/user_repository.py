import uuid
from typing import Any, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self,
        count: int,
        page: int,
        **kwargs: Any,
    ) -> tuple[list[User], int]:
        stmt = select(User)

        if "username" in kwargs and kwargs["username"]:
            stmt = stmt.where(User.username == kwargs["username"])

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.session.execute(total_stmt)
        total = total_result.scalar_one()

        offset = (page - 1) * count
        stmt = stmt.offset(offset).limit(count)

        result = await self.session.execute(stmt)
        users: Sequence[User] = result.scalars().all()
        return list(users), total

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        if user_data.username is not None:
            user.username = user_data.username
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.description is not None:
            user.description = user_data.description

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: uuid.UUID) -> None:
        user = await self.get_by_id(user_id)
        if user is None:
            return
        await self.session.delete(user)
        await self.session.commit()
