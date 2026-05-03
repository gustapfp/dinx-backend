import jwt
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.auth.models import Users
from src.app.auth.schemas import oauth2_scheme
from src.app.auth.utils.helper import TokenHelper
from src.config.db import get_session

token_helper = TokenHelper()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """Decode the Bearer token and return the authenticated user.

    Args:
        token (str): The JWT token extracted from the Authorization header.
        session (AsyncSession): The async database session.

    Returns:
        Users: The authenticated user instance.

    Raises:
        HTTPException: 401 if the token is invalid, expired, or the user does not exist.
    """
    try:
        payload = token_helper.decode_token(token)
        if payload.get("type") != "access":
            raise credentials_exception
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    result = await session.exec(select(Users).where(Users.email == email))
    user = result.first()
    if user is None:
        raise credentials_exception
    return user
