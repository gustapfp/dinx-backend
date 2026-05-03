from datetime import timedelta

import jwt
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.auth.models import RefreshToken, Users
from src.app.auth.schemas import TokenPair, UserCreate, UserResponse
from src.app.auth.utils.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from src.app.auth.utils.helper import PasswordHelper, TokenHelper

password_helper = PasswordHelper()
token_helper = TokenHelper()

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    async def register(self, body: UserCreate, session: AsyncSession) -> UserResponse:
        """Create a new user account.

        Args:
            body (UserCreate): Registration payload.
            session (AsyncSession): Database session.

        Returns:
            UserResponse: The created user.

        Raises:
            HTTPException: 400 if the email is already registered.
        """
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

    async def login(self, email: str, password: str, session: AsyncSession) -> TokenPair:
        """Validate credentials and return an access + refresh token pair.

        Args:
            email (str): User email.
            password (str): Plain-text password.
            session (AsyncSession): Database session.

        Returns:
            TokenPair: Access token and refresh token.

        Raises:
            HTTPException: 401 if credentials are invalid.
        """
        result = await session.exec(select(Users).where(Users.email == email))
        user = result.first()

        if not user or not password_helper.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = token_helper.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token, expires_at = token_helper.create_refresh_token(data={"sub": user.email})

        session.add(RefreshToken(token=refresh_token, user_id=user.id, expires_at=expires_at))
        await session.commit()

        return TokenPair(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    async def refresh(self, refresh_token: str, session: AsyncSession) -> str:
        """Issue a new access token from a valid refresh token.

        Args:
            refresh_token (str): The refresh token from the client.
            session (AsyncSession): Database session.

        Returns:
            str: New access token.

        Raises:
            HTTPException: 401 if the token is invalid, expired, or revoked.
        """
        try:
            payload = token_helper.decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise _credentials_error
            email: str | None = payload.get("sub")
            if not email:
                raise _credentials_error
        except jwt.InvalidTokenError:
            raise _credentials_error

        result = await session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token))
        db_token = result.first()
        if not db_token or db_token.revoked:
            raise _credentials_error

        return token_helper.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    async def logout(self, refresh_token: str, session: AsyncSession) -> None:
        """Revoke a refresh token, preventing it from issuing new access tokens.

        Args:
            refresh_token (str): The refresh token to revoke.
            session (AsyncSession): Database session.
        """
        result = await session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token))
        db_token = result.first()
        if db_token:
            db_token.revoked = True
            await session.commit()
