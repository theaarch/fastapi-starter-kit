from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_update_password_success():
    hashed = get_password_hash("OldPassword123!")
    now = datetime.now(UTC)
    mock_user = User(
        id=5,
        name="Charlie",
        email="charlie@example.com",
        password=hashed,
        email_verified_at=None,
        created_at=now,
        updated_at=now,
    )

    mock_db = AsyncMock()

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
            f"{settings.API_PREFIX}/auth/user/password",
            headers={"Authorization": "Bearer fake-token"},
            json={
                "current_password": "OldPassword123!",
                "password": "NewPassword123!",
                "password_confirmation": "NewPassword123!",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"


@pytest.mark.asyncio
async def test_update_password_wrong_current():
    hashed = get_password_hash("OldPassword123!")
    now = datetime.now(UTC)
    mock_user = User(
        id=5,
        name="Charlie",
        email="charlie@example.com",
        password=hashed,
        email_verified_at=None,
        created_at=now,
        updated_at=now,
    )

    mock_db = AsyncMock()

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
            f"{settings.API_PREFIX}/auth/user/password",
            headers={"Authorization": "Bearer fake-token"},
            json={
                "current_password": "WrongPassword!",
                "password": "NewPassword123!",
                "password_confirmation": "NewPassword123!",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect current password"


@pytest.mark.asyncio
async def test_update_password_mismatch():
    mock_db = AsyncMock()

    async def override_current_user():
        return User(id=5, name="C", email="c@e.com", password="hash")

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.put(
            f"{settings.API_PREFIX}/auth/user/password",
            headers={"Authorization": "Bearer fake-token"},
            json={
                "current_password": "OldPassword123!",
                "password": "NewPassword123!",
                "password_confirmation": "MismatchedPassword123!",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 422
