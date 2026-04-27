from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.auth.models import Users
from src.app.auth.schemas import Token, UserCreate, UserResponse
from src.app.auth.utils.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from src.app.auth.utils.deps import get_current_user
from src.app.auth.utils.helper import PasswordHelper, TokenHelper
from src.config.db import get_session

password_helper = PasswordHelper()
token_helper = TokenHelper()

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    result = await session.exec(select(Users).where(Users.email == body.email))
    if result.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = Users(
        email=body.email,
        password=password_helper.hash_password(body.password),
        first_name=body.first_name,
        last_name=body.last_name,
        role=body.role,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserResponse.model_validate(user)


@auth_router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Token:
    result = await session.exec(select(Users).where(Users.email == form.username))
    user = result.first()

    if not user or not password_helper.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = token_helper.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/logout")
async def logout(_current_user: Users = Depends(get_current_user)) -> dict:
    return {"message": "Logout successful"}


@auth_router.get("/me", response_model=UserResponse)
async def me(current_user: Users = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
