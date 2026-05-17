from pydantic import BaseModel
from typing import Optional


class CheckInCreate(BaseModel):

    quarter: str

    planned_value: float

    actual_value: float

    employee_comment: Optional[str] = None

    goal_id: int