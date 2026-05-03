from enum import Enum

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
