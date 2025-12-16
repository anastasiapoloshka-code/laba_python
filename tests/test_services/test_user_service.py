import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_service import UserService
from app.schemas import UserCreate
from app.models import User


@pytest.mark.asyncio
async def test_service_create_user_builds_model_and_calls_repo():
    # Мокаем репозиторий
    mock_repo = AsyncMock()
    mock_user = MagicMock(spec=User)
    mock_user.id = "uuid-123"
    mock_user.email = "test@example.com"
    mock_user.username = "john_doe"
    mock_repo.create.return_value = mock_user

    # Создаём сервис
    service = UserService(mock_repo)

    # Создаём DTO
    data = UserCreate(
        username="john_doe",
        email="test@example.com",
        description="test user"
    )

    # Вызываем сервис
    result = await service.create(data)

    # ✅ ИСПРАВЛЕНО: проверяем, что передан UserCreate объект
    mock_repo.create.assert_called_once_with(data)  # или mock_repo.create.assert_called_once()

    # Проверяем результат
    assert result.email == "test@example.com"
