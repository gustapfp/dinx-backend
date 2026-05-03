from datetime import datetime

from sqlmodel import Field

from src.app.auth.schemas import UserRole
from src.config.models import DinxBaseModel


class Users(DinxBaseModel, table=True):
    email: str
    password: str
    first_name: str
    last_name: str
    active: bool = True
    role: UserRole = UserRole.USER


class RefreshToken(DinxBaseModel, table=True):
    token: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime
    revoked: bool = False
