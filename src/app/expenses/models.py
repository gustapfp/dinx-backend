from enum import Enum
from sqlmodel import Field
from datetime import datetime
from src.config.models import BaseModel


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(BaseModel, table=True):
    type: TransactionType = Field(default=TransactionType.EXPENSE)
    amount: float = Field(default=0.0)
    date: datetime = Field(default=datetime.now())
    name: str = Field(default="")
    description: str = Field(default="")
    category: str = Field(default="")
