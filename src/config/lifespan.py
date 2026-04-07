from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.db import create_db_and_tables

import src.app.budgets.models  # noqa: F401
import src.app.expenses.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
