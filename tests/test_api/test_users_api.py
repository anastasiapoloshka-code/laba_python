import pytest
from pydantic import BaseModel
from litestar import get
from litestar.status_codes import HTTP_200_OK
from litestar.testing import create_test_client

class UserCreate(BaseModel):
    username: str
    email: str
    description: str | None = None

@get("/users")
def get_users() -> dict:
    return {"items": [], "total": 0}

def test_get_users_initial():
    """GET /users - базовый список"""
    with create_test_client(route_handlers=[get_users]) as client:
        response = client.get("/users")
        print(f"GET /users: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data

def test_create_user_simple():
    """Простой POST тест"""
    with create_test_client(route_handlers=[get_users]) as client:
        response = client.post("/users", json={
            "username": "john_doe",
            "email": "test@example.com"
        })
        print(f"POST /users: {response.status_code}")
        assert response.status_code == 405  # Ожидаем 405 (метод не найден)
