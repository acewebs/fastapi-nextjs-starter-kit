import pytest


@pytest.mark.asyncio
async def test_list_records_empty(client):
    response = await client.get("/api/v1/records")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_record(client):
    response = await client.post(
        "/api/v1/records",
        json={
            "name": "Test Record",
            "description": "A test description",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item"]["name"] == "Test Record"
    assert data["item"]["description"] == "A test description"
    assert data["item"]["status"] == "pending"
    assert "id" in data["item"]
    assert "created_at" in data["item"]


@pytest.mark.asyncio
async def test_create_record_validation(client):
    response = await client.post("/api/v1/records", json={"name": ""})
    assert response.status_code == 422

    response = await client.post("/api/v1/records", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_record(client):
    create = await client.post("/api/v1/records", json={"name": "Get Me"})
    record_id = create.json()["item"]["id"]

    response = await client.get(f"/api/v1/records/{record_id}")
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Get Me"


@pytest.mark.asyncio
async def test_get_record_not_found(client):
    response = await client.get("/api/v1/records/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_record(client):
    create = await client.post("/api/v1/records", json={"name": "Original"})
    record_id = create.json()["item"]["id"]

    response = await client.patch(
        f"/api/v1/records/{record_id}",
        json={
            "name": "Updated",
            "status": "completed",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == "Updated"
    assert data["item"]["status"] == "completed"


@pytest.mark.asyncio
async def test_update_record_partial(client):
    create = await client.post(
        "/api/v1/records",
        json={
            "name": "Original",
            "description": "Keep this",
        },
    )
    record_id = create.json()["item"]["id"]

    response = await client.patch(
        f"/api/v1/records/{record_id}",
        json={
            "name": "Changed",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == "Changed"
    assert data["item"]["description"] == "Keep this"


@pytest.mark.asyncio
async def test_delete_record(client):
    create = await client.post("/api/v1/records", json={"name": "Delete Me"})
    record_id = create.json()["item"]["id"]

    response = await client.delete(f"/api/v1/records/{record_id}")
    assert response.status_code == 204

    response = await client.get(f"/api/v1/records/{record_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_records_with_data(client):
    await client.post("/api/v1/records", json={"name": "First"})
    await client.post("/api/v1/records", json={"name": "Second"})
    await client.post("/api/v1/records", json={"name": "Third"})

    response = await client.get("/api/v1/records")
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


@pytest.mark.asyncio
async def test_list_records_pagination(client):
    for i in range(5):
        await client.post("/api/v1/records", json={"name": f"Record {i}"})

    response = await client.get("/api/v1/records?skip=0&limit=2")
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
