import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ---------- Базовые схемы ----------

class UserBase(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    description: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    description: str | None = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    total: int
    items: list[UserResponse]
