import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_app_info(client):
    response = await client.get("/api/v1/app")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "env" in data
    assert "version" in data
