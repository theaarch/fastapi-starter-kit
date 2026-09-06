from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token, get_password_hash
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_api_login_success():
    hashed = get_password_hash("password123")
    now = datetime.now(UTC)
    mock_user = User(
        id=10,
        name="Alice",
        email="test@example.com",
        email_verified_at=None,
        password=hashed,
        created_at=now,
        updated_at=now,
    )

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    decoded = decode_access_token(data["access_token"])
    assert decoded["sub"] == "10"
    assert decoded["name"] == "Alice"
    assert decoded["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_api_login_wrong_password():
    hashed = get_password_hash("correctPassword")
    now = datetime.now(UTC)
    mock_user = User(
        id=10,
        name="Alice",
        email="test@example.com",
        email_verified_at=None,
        password=hashed,
        created_at=now,
        updated_at=now,
    )

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/login",
            json={"email": "test@example.com", "password": "wrongPassword"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_api_login_user_not_found():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/login",
            json={"email": "nonexistent@example.com", "password": "anyPassword"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
