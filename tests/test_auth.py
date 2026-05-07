import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Passw0rd!",
        "role": "MEMBER",
    }
    res = await client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "password" not in data

    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
    )
    assert login_res.status_code == 200
    token = login_res.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "Passw0rd!",
        "role": "MEMBER",
    }
    await client.post("/api/v1/auth/register", json=payload)
    res = await client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    payload = {
        "username": "wrongpwd",
        "email": "wrong@example.com",
        "password": "Passw0rd!",
        "role": "MEMBER",
    }
    await client.post("/api/v1/auth/register", json=payload)
    res = await client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": "BadPass1!"},
    )
    assert res.status_code == 401
