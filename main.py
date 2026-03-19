from fastapi import FastAPI
from src.app.auth.router import auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
