import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class UserListResponse(BaseModel):
    total: int
    items: List[UserResponse]
