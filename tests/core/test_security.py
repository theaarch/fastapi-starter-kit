from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from main import app


def test_password_hashing():
    raw_password = "mySecretPassword123!"
    hashed = get_password_hash(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_jwt_token_flow():
    user_id = 42
    token = create_access_token(
        subject=user_id,
        expires_delta=timedelta(minutes=15),
        extra_claims={"name": "Alice", "email": "user@example.com"},
    )
    assert isinstance(token, str)

    payload = decode_access_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["name"] == "Alice"
    assert payload["email"] == "user@example.com"
    assert "exp" in payload
    assert "iat" in payload


def test_jwt_token_expiration():
    expired_token = create_access_token(
        subject=1,
        expires_delta=timedelta(minutes=-1),
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(expired_token)


@pytest.mark.asyncio
async def test_real_token_dependency_resolution():
    token = create_access_token(subject=99)
    now = datetime.now(UTC)
    mock_user = User(
        id=99,
        name="TokenUser",
        email="token@example.com",
        password="hash",
        email_verified_at=None,
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
        response = await ac.get(
            f"{settings.API_PREFIX}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == 99
    assert response.json()["name"] == "TokenUser"
