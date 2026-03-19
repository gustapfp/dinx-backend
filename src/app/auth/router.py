from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post("/login")
def login(request):
    return {"message": "Login successful"}


@auth_router.post("/register")
def register(request):
    return {"message": "Register successful"}


@auth_router.post("/logout")
def logout(request):
    return {"message": "Logout successful"}
