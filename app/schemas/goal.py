from pydantic import BaseModel

class GoalCreate(BaseModel):

    title: str
    description: str
    uom: str
    target_value: int
    weightage: int
    employee_id: int