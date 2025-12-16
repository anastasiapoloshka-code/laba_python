import uuid
from typing import Any

from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.models import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(
        self,
        count: int,
        page: int,
        **kwargs: Any,
    ):
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: uuid.UUID) -> None:
        await self.user_repository.delete(user_id)
