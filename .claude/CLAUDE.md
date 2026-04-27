# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```bash
uv sync
```

**Run locally (without Docker):**
```bash
uvicorn main:app --reload
```

**Preferd: Run with Docker (full stack: FastAPI + PostgreSQL):**
```bash
docker-compose -f compose/local/local.yml up
```

**Type checking:**
```bash
mypy src/
```

**Run tests:**
```bash
pytest
pytest tests/path/to/test_file.py::test_function_name  # single test
```

## Architecture

**Stack:** FastAPI + SQLModel (SQLAlchemy + Pydantic) + PostgreSQL 17 (async via asyncpg) + JWT auth (PyJWT + Passlib/bcrypt)

**Entry point:** `main.py` — instantiates the FastAPI app, registers routers, and delegates startup/shutdown to `src/config/lifespan.py` (creates DB tables on startup).

**Module layout under `src/`:**
- `config/` — database session factory (`database.py`), app settings from env vars (`settings.py`), base SQLModel (`base.py`), and lifespan handler
- `app/auth/` — the only fully-implemented domain: register/login endpoints (`router.py`), JWT + password helpers (`helpers.py`), Pydantic schemas (`schemas.py`), and ORM model (`models.py`)
- `app/budgets/`, `app/expenses/` — domain models defined, no endpoints yet
- `app/investments/`, `app/metrics/`, `app/users/` — stubs, empty

**Base model:** `DinxBaseModel` in `src/config/base.py` provides `id` (UUID PK), `created_at`, and `updated_at` for all domain models.

**Async pattern:** Database sessions are async (`AsyncSession`); always use `await` for DB operations. Session dependency is injected via FastAPI's `Depends`.

**Auth flow:** `POST /auth/register` creates a user with hashed password → `POST /auth/login` validates credentials and returns a JWT access token. Token helpers live in `src/app/auth/helpers.py`.

## Environment

Secrets are loaded from two env files (used by Docker Compose and mapped in `src/config/settings.py`):
- `.envs/.local/.postgres` — `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `.envs/.local/.fastapi` — `SECRET_KEY`, `JWT_ALGORITHM`

These files must exist before running locally or via Docker.

## Code Style

Only add comments to complex code where the intent is non-obvious.

## mypy

`mypy_path = "src"` is set in `pyproject.toml`, so imports like `from config.settings import settings` resolve correctly without the `src.` prefix.
