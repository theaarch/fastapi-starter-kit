import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "message" in response.json()
