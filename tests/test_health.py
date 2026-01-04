from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_health(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Testing sync endpoints (if we don’t want async)
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_sync():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

