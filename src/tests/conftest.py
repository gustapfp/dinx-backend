import os
import tempfile
from collections.abc import AsyncGenerator

# Must be set before any app import so pydantic-settings can read them
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from main import app
from src.config.db import get_session

# Import all models so SQLModel.metadata knows about them before create_all
import src.app.auth.models  # noqa: F401


@pytest.fixture
async def engine():
    """Create a fresh file-based SQLite database for each test.

    File-based SQLite (instead of :memory:) ensures all sessions share the
    same data, which mirrors how PostgreSQL works in production.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    # NullPool is required for file-based SQLite: the default pool caches
    # connections whose transaction snapshots predate other sessions' commits,
    # causing selects to miss rows that were just inserted and committed.
    _engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        echo=False,
        poolclass=NullPool,
    )
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield _engine
    await _engine.dispose()
    os.unlink(db_path)


@pytest.fixture
async def client(engine) -> AsyncGenerator[AsyncClient, None]:
    """Provide an AsyncClient whose requests use the test database.

    Each request gets a fresh session from the test engine, matching
    how the real app creates sessions via get_session.
    """
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Override that creates a new session per request from the test engine."""
        async with session_maker() as _session:
            yield _session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Reusable data helpers
# ---------------------------------------------------------------------------

USER_PAYLOAD = {
    "email": "test@example.com",
    "password": "strongpassword123",
    "first_name": "Test",
    "last_name": "User",
}


@pytest.fixture
async def registered_user(client: AsyncClient) -> dict:
    """Register a user and return the response body."""
    response = await client.post("/auth/register", json=USER_PAYLOAD)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def tokens(client: AsyncClient, registered_user: dict) -> dict:
    """Log in and return the token pair."""
    response = await client.post(
        "/auth/login",
        data={"username": USER_PAYLOAD["email"], "password": USER_PAYLOAD["password"]},
    )
    assert response.status_code == 200
    return response.json()
