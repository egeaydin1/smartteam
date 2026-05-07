import pytest


async def _register_and_login(client, suffix: str, role: str = "MEMBER") -> str:
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": f"{suffix}@example.com",
            "password": "Passw0rd!",
            "role": role,
        },
    )
    res = await client.post(
        "/api/v1/auth/login",
        data={"username": f"{suffix}@example.com", "password": "Passw0rd!"},
    )
    return res.json()["access_token"]


@pytest.mark.asyncio
async def test_create_and_list_project(client):
    token = await _register_and_login(client, "proj_owner", "ADMIN")
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/projects/",
        json={"title": "Test Project", "description": "A description"},
        headers=headers,
    )
    assert res.status_code == 201
    project = res.json()
    assert project["title"] == "Test Project"

    list_res = await client.get("/api/v1/projects/", headers=headers)
    assert list_res.status_code == 200
    assert any(p["id"] == project["id"] for p in list_res.json())


@pytest.mark.asyncio
async def test_update_project_forbidden(client):
    owner_token = await _register_and_login(client, "owner2", "ADMIN")
    other_token = await _register_and_login(client, "other2", "MEMBER")

    res = await client.post(
        "/api/v1/projects/",
        json={"title": "Owner Project"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    project_id = res.json()["id"]

    patch_res = await client.patch(
        f"/api/v1/projects/{project_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert patch_res.status_code == 403
