from pydantic import BaseModel
from typing import List


class GoalUpdateItem(BaseModel):

    goal_id: int

    target_value: float

    weightage: int


class ManagerBulkGoalUpdate(BaseModel):

    employee_id: int

    goals: List[GoalUpdateItem]