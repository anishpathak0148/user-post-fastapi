import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Testing sync endpoints (if we don’t want async)


client = TestClient(app)


def test_health_sync():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
