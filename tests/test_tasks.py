import pytest


async def _setup(client) -> tuple[str, int]:
    """Register admin, create a project; return (token, project_id)."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "task_admin",
            "email": "task_admin@example.com",
            "password": "Passw0rd!",
            "role": "ADMIN",
        },
    )
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": "task_admin@example.com", "password": "Passw0rd!"},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = await client.post(
        "/api/v1/projects/", json={"title": "Task Project"}, headers=headers
    )
    return token, project.json()["id"]


@pytest.mark.asyncio
async def test_create_and_advance_task(client):
    token, project_id = await _setup(client)
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        f"/api/v1/projects/{project_id}/tasks/",
        json={"title": "Write tests", "priority": "HIGH"},
        headers=headers,
    )
    assert res.status_code == 201
    task = res.json()
    assert task["status"] == "TO_DO"

    advance = await client.post(
        f"/api/v1/projects/{project_id}/tasks/{task['id']}/advance",
        headers=headers,
    )
    assert advance.status_code == 200
    assert advance.json()["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_task_not_found(client):
    token, project_id = await _setup(client)
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.get(
        f"/api/v1/projects/{project_id}/tasks/99999", headers=headers
    )
    assert res.status_code == 404
