from fastapi import APIRouter, Depends

from src.app.auth.models import Users
from src.app.auth.utils.deps import get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/login")
def login(request):
    return {"message": "Login successful"}


@auth_router.post("/register")
def register(request):
    return {"message": "Register successful"}


@auth_router.post("/logout")
def logout(request):
    return {"message": "Logout successful"}


@auth_router.get("/me")
async def me(current_user: Users = Depends(get_current_user)):
    return current_user
