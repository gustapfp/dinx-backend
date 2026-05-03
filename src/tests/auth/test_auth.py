import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------

async def test_register_success(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "password": "secret123",
            "first_name": "New",
            "last_name": "User",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert body["first_name"] == "New"
    assert body["active"] is True
    assert "password" not in body


async def test_register_duplicate_email(client: AsyncClient, registered_user: dict) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "email": registered_user["email"],
            "password": "anotherpassword",
            "first_name": "Dup",
            "last_name": "User",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

async def test_login_success(client: AsyncClient, registered_user: dict) -> None:
    response = await client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, registered_user: dict) -> None:
    response = await client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_login_unknown_email(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/login",
        data={"username": "nobody@example.com", "password": "irrelevant"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /auth/refresh
# ---------------------------------------------------------------------------

async def test_refresh_success(client: AsyncClient, tokens: dict) -> None:
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    # New access token must differ from the original
    assert body["access_token"] != tokens["access_token"]


async def test_refresh_with_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": "this.is.not.valid"},
    )
    assert response.status_code == 401


async def test_refresh_with_access_token_rejected(client: AsyncClient, tokens: dict) -> None:
    """An access token must not be accepted on the refresh endpoint."""
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["access_token"]},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /auth/logout
# ---------------------------------------------------------------------------

async def test_logout_success(client: AsyncClient, tokens: dict) -> None:
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert response.status_code == 204


async def test_logout_revokes_refresh_token(client: AsyncClient, tokens: dict) -> None:
    """After logout the refresh token must no longer work."""
    await client.post(
        "/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert response.status_code == 401


async def test_logout_requires_auth(client: AsyncClient, tokens: dict) -> None:
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /auth/me
# ---------------------------------------------------------------------------

async def test_me_success(client: AsyncClient, tokens: dict) -> None:
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "test@example.com"
    assert "password" not in body


async def test_me_without_token(client: AsyncClient) -> None:
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_me_with_invalid_token(client: AsyncClient) -> None:
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401


async def test_me_with_refresh_token_rejected(client: AsyncClient, tokens: dict) -> None:
    """A refresh token must not grant access to protected endpoints."""
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert response.status_code == 401
