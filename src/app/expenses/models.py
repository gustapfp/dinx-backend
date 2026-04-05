from enum import Enum
from sqlmodel import Field, ForeignKey
from datetime import datetime
from src.config.models import DinxBaseModel


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(DinxBaseModel, table=True):
    type: TransactionType = Field(default=TransactionType.EXPENSE)
    amount: float = Field(default=0.0)
    date: datetime = Field(default=datetime.now())
    name: str = Field(default="")
    description: str = Field(default="")
    income_category: str | None = Field(ForeignKey("budget_category.name"))
    expense_category: str | None = Field(ForeignKey("investment_category.name"))
