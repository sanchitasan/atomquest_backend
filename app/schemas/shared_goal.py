from pydantic import BaseModel
from typing import List


class SharedGoalCreate(BaseModel):

    title: str

    description: str

    thrust_area: str

    uom: str

    target_value: float

    weightage: float

    employee_ids: List[int]

    primary_owner_id: int