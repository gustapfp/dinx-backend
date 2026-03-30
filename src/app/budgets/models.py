from datetime import datetime
from turtle import color
from unicodedata import category
from pydantic import model_validator
from sqlmodel import Field, ForeignKey
from src.config.models import BaseModel


class Budget(BaseModel, table=True):
    category_name: str = Field(ForeignKey("budget_category.name"))
    expended_amount: float = Field(default=0.0)
    monthly_limit: float = Field(default=0.0)


class BudgetCategory(BaseModel, table=True):
    icon: str = Field()
    name: str = Field()
    default_color: str = Field()
    active: bool = Field(default=True)
    total_expended: float = Field(default=0.0)


class BudgetCategoryHistory(BaseModel, table=True):
    start_at: datetime
    end_at: datetime
    category_name: str = Field(ForeignKey("budget_category.name"))
    total_expended: float = Field(default=0.0)
    acumulated_limit: float = Field(default=0.0)

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_at < self.start_at:
            raise ValueError("end_at must be greater than or equal to start_at")
        return self
