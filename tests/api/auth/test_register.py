from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_register_success():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    async def mock_refresh(user: User):
        user.id = 1
        user.created_at = datetime.now(UTC)
        user.updated_at = datetime.now(UTC)

    mock_db.refresh.side_effect = mock_refresh

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/register",
            json={
                "name": "Bob",
                "email": "bob@example.com",
                "password": "SecurePassword123!",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"
    assert "password" not in data
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_register_duplicate_email():
    existing_user = User(
        id=2,
        name="Existing",
        email="taken@example.com",
        password="hash",
    )
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_user
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/register",
            json={
                "name": "Bob",
                "email": "taken@example.com",
                "password": "SecurePassword123!",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
