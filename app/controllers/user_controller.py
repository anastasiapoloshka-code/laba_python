import uuid
from typing import List

from litestar import Controller, get, post, put, delete
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException

from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: uuid.UUID = Parameter(),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, ge=1, le=100),
        page: int = Parameter(default=1, ge=1),
    ) -> UserListResponse:
        """Получить список пользователей + total"""
        users, total = await user_service.get_by_filter(count=count, page=page)
        items = [UserResponse.model_validate(u) for u in users]
        return UserListResponse(total=total, items=items)

    @post()
    async def create_user(
        self,
        user_service: UserService,
        user_data: UserCreate = Body(),
    ) -> UserResponse:
        user = await user_service.create(user_data)
        return UserResponse.model_validate(user)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: uuid.UUID,
        user_data: UserUpdate = Body(),
    ) -> UserResponse:
        user = await user_service.update(user_id, user_data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: uuid.UUID,
    ) -> None:
        await user_service.delete(user_id)
        return None
