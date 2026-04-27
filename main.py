from fastapi import FastAPI
from src.config.lifespan import lifespan
from src.app.auth.router import auth_router

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
