from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, count: int = 10, page: int = 1) -> Tuple[List[User], int]:
        offset = (page - 1) * count
        result = await self.db_session.execute(select(User).limit(count).offset(offset))
        users = result.scalars().all()
        total_result = await self.db_session.execute(select(User))
        total = total_result.scalar()
        return users, total or 0
