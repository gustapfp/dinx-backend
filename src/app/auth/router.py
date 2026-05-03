from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.auth.models import Users
from src.app.auth.schemas import Token, TokenPair, UserCreate, UserResponse
from src.app.auth.services import AuthService
from src.app.auth.utils.deps import get_current_user
from src.config.db import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    return await auth_service.register(body, session)


@auth_router.post("/login", response_model=TokenPair)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    return await auth_service.login(form.username, form.password, session)


@auth_router.post("/refresh", response_model=Token)
async def refresh(
    refresh_token: str = Body(..., embed=True),
    session: AsyncSession = Depends(get_session),
) -> Token:
    access_token = await auth_service.refresh(refresh_token, session)
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    refresh_token: str = Body(..., embed=True),
    _current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    await auth_service.logout(refresh_token, session)


@auth_router.get("/me", response_model=UserResponse)
async def me(current_user: Users = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
