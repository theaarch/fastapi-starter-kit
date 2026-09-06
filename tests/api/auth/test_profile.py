from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_get_profile_me():
    now = datetime.now(UTC)
    mock_user = User(
        id=5,
        name="Charlie",
        email="charlie@example.com",
        password="hash",
        email_verified_at=None,
        created_at=now,
        updated_at=now,
    )

    async def override_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.get(
            f"{settings.API_PREFIX}/auth/me",
            headers={"Authorization": "Bearer fake-token"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 5
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"


@pytest.mark.asyncio
async def test_update_profile_me():
    now = datetime.now(UTC)
    mock_user = User(
        id=5,
        name="Old Name",
        email="old@example.com",
        password="hash",
        email_verified_at=None,
        created_at=now,
        updated_at=now,
    )

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    async def override_current_user():
        return mock_user

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.put(
            f"{settings.API_PREFIX}/auth/me",
            headers={"Authorization": "Bearer fake-token"},
            json={"name": "New Name", "email": "new@example.com"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "new@example.com"
