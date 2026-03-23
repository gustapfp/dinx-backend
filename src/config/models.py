from datetime import datetime
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    __abstract__ = True
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
