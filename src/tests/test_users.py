import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_create_user(client: AsyncClient):

    org_payload = {"name": "Test Org User", "description": "Org for users"}
    org_response = await client.post("/organizations/", json=org_payload)
    org_data = org_response.json()

    org_id = org_data["_id"]

    user_payload = {
        "email": "user1@example.com",
        "full_name": "User One",
        "role": "reader"
    }

    response = await client.post(f"/organizations/{org_id}/users/",
                                 json=user_payload)
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == user_payload["email"]
    assert data["role"] == "reader"
    assert data["org"]["name"] == "Test Org User"


async def test_create_duplicate_user(client: AsyncClient):

    org_payload = {"name": "DupUserOrg", "description": "Dup test"}
    org_response = await client.post("/organizations/", json=org_payload)
    org_id = org_response.json()["_id"]

    user_payload = {
        "email": "dup@example.com",
        "full_name": "Dup User",
        "role": "writer"
    }
    await client.post(f"/organizations/{org_id}/users/", json=user_payload)

    response = await client.post(f"/organizations/{org_id}/users/",
                                 json=user_payload)
    assert response.status_code == 409
    assert "already exists" in response.text


async def test_list_users(client: AsyncClient):
    org_payload = {"name": "ListUserOrg", "description": "Listing test"}
    org_response = await client.post("/organizations/", json=org_payload)
    org_id = org_response.json()["_id"]

    for i in range(2):
        user_payload = {
            "email": f"user{i}@example.com",
            "full_name": f"User {i}",
            "role": "reader",
        }
        await client.post(f"/organizations/{org_id}/users/", json=user_payload)

    response = await client.get(f"/organizations/{org_id}/users/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all("email" in user for user in data)
