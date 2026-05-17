from pydantic import BaseModel, EmailStr


class GoalCreate(BaseModel):
    title: str
    description: str
    thrust_area: str
    uom: str
    target_value: int
    weightage: int
    manager_email: EmailStr


class GoalResponse(BaseModel):
    id: int
    title: str
    description: str
    thrust_area: str
    uom: str
    target_value: int
    weightage: int
    status: str
    employee_id: int
    is_locked: bool
    manager_id: int | None = None
    approved_by: int | None = None

    class Config:
        from_attributes = True
