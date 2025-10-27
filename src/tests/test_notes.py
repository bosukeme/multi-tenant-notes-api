import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def setup_org_and_users(client: AsyncClient):

    org_payload = {"name": "Note Org", "description": "For note tests"}
    org_response = await client.post("/organizations/", json=org_payload)
    org_data = org_response.json()
    org_id = org_data["_id"]

    writer_payload = {
        "email": "writer@example.com",
        "full_name": "Writer User",
        "role": "writer",
    }
    writer_res = await client.post(
        f"/organizations/{org_id}/users/", json=writer_payload
    )
    writer_data = writer_res.json()

    reader_payload = {
        "email": "reader@example.com",
        "full_name": "Reader User",
        "role": "reader",
    }
    reader_res = await client.post(
        f"/organizations/{org_id}/users/", json=reader_payload
    )
    reader_data = reader_res.json()

    admin_payload = {
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role": "admin",
    }
    admin_res = await client.post(
        f"/organizations/{org_id}/users/", json=admin_payload
    )
    admin_data = admin_res.json()

    return org_data, writer_data, reader_data, admin_data


async def test_create_note_as_writer(client: AsyncClient):
    org, writer, _, _ = await setup_org_and_users(client)

    headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": writer["_id"],
    }

    note_payload = {
        "title": "Writer's Note",
        "content": "This note was created by the writer role.",
    }

    response = await client.post(
        "/notes/",
        json=note_payload,
        headers=headers,
    )

    data = response.json()
    assert response.status_code == 201
    assert data["title"] == note_payload["title"]
    assert data["author"]["email"] == writer["email"]
    assert data["org"]["name"] == org["name"]


async def test_reader_cannot_create_note(client: AsyncClient):
    org, _, reader, _ = await setup_org_and_users(client)

    headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": reader["_id"],
    }

    note_payload = {
        "title": "Reader Note",
        "content": "Readers should not be able to create notes.",
    }

    response = await client.post(
        "/notes/",
        json=note_payload,
        headers=headers,
    )

    assert response.status_code == 403


async def test_list_notes(client: AsyncClient):
    org, writer, reader, _ = await setup_org_and_users(client)

    writer_headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": writer["_id"],
    }
    reader_headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": reader["_id"],
    }

    for i in range(2):
        note_payload = {
            "title": f"Note {i}",
            "content": f"Writer created note {i}",
        }
        await client.post(
            "/notes/",
            json=note_payload,
            headers=writer_headers,
        )

    response = await client.get("/notes/", headers=reader_headers)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all("title" in note for note in data)


async def test_admin_can_delete_note(client: AsyncClient):
    org, writer, _, admin = await setup_org_and_users(client)

    writer_headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": writer["_id"],
    }
    admin_headers = {
        "X-Org-ID": org["_id"],
        "X-User-ID": admin["_id"],
    }

    note_payload = {"title": "Delete Me", "content": "To be deleted."}
    note_res = await client.post(
        "/notes/",
        json=note_payload,
        headers=writer_headers,
    )
    note_id = note_res.json()["_id"]

    delete_res = await client.delete(
        f"/notes/{note_id}",
        headers=admin_headers,
    )

    assert delete_res.status_code == 204


async def test_cross_organization_access_denied(client: AsyncClient):
    org_a, writer_a, _, _ = await setup_org_and_users(client)

    headers_a = {
        "X-Org-ID": org_a["_id"],
        "X-User-ID": writer_a["_id"],
    }

    note_payload = {
        "title": "Org A Secret",
        "content": "This should not be accessible from Org B.",
    }

    note_res = await client.post("/notes/", json=note_payload,
                                 headers=headers_a)
    note_id = note_res.json()["_id"]

    org_b_payload = {"name": "Other Org", "description": "Second organization"}
    org_b_res = await client.post("/organizations/", json=org_b_payload)
    org_b_id = org_b_res.json()["_id"]

    user_b_payload = {
        "email": "intruder@example.com",
        "full_name": "Intruder",
        "role": "reader",
    }
    user_b_res = await client.post(
        f"/organizations/{org_b_id}/users/", json=user_b_payload
    )
    user_b_data = user_b_res.json()

    headers_b = {
        "X-Org-ID": org_b_id,
        "X-User-ID": user_b_data["_id"],
    }

    cross_res = await client.get(f"/notes/{note_id}", headers=headers_b)
    assert cross_res.status_code == 401
    assert "Unauthorized access" in cross_res.text
