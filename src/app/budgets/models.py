from turtle import color
from unicodedata import category
from sqlmodel import Field, ForeignKey
from src.config.models import BaseModel


class Budget(BaseModel, table=True):
    category: str = Field(ForeignKey("budget_category.name"))
    expended_amount: float = Field(default=0.0)
    monthly_limit: float = Field(default=0.0)


class BudgetCategory(BaseModel, table=True):
    icon: str = Field()
    name: str = Field()
    color: str = Field()  # noqa: F811
    active: bool = Field(default=True)
    total_expended: float = Field(default=0.0)
