from typing import List, Tuple

from app.repositories.user_repository import UserRepository
from app.schemas import UserListResponse, UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_filter(self, count: int, page: int) -> Tuple[List[dict], int]:
        users, total = await self.user_repository.get_all(count, page)
        return users, total
