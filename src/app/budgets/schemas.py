from datetime import datetime
from pydantic import BaseModel


class BudgetHistorySchema(BaseModel):
    category_name: str
    total_expended: str
    total_limit: float
    started_at: datetime
    ended_at: datetime
