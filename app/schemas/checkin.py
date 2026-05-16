from pydantic import BaseModel

class CheckInCreate(BaseModel):

    quarter: str
    progress: int
    remarks: str
    goal_id: int