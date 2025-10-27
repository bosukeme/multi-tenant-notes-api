import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_create_organization(client: AsyncClient):
    payload = {"name": "Test Org", "description": "A sample organization"}
    response = await client.post("/organizations/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Org"
    assert "created_at" in data
    assert "_id" in data or "id" in data


async def test_create_duplicate_organization(client: AsyncClient):
    payload = {"name": "Dup Org", "description": "Duplicate"}
    await client.post("/organizations/", json=payload)
    response = await client.post("/organizations/", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.text


async def test_list_organizations(client: AsyncClient):

    await client.post("/organizations/", json={"name": "Org1"})
    await client.post("/organizations/", json={"name": "Org2"})

    response = await client.get("/organizations/")
    assert response.status_code == 200
    orgs = response.json()

    assert isinstance(orgs, list)
    assert len(orgs) >= 2
    assert all("name" in o for o in orgs)
