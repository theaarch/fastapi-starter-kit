import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_logout_success():
    mock_user = User(id=1, name="Test", email="test@example.com", password="hash")

    async def override_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            f"{settings.API_PREFIX}/auth/logout",
            headers={"Authorization": "Bearer fake-token"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"
