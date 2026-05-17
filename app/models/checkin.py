from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Text,
    DateTime
)

from datetime import datetime
from app.database import Base

class CheckIn(Base):

    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    quarter = Column(String(10))
    planned_value = Column(Float)
    actual_value = Column(Float)
    progress_score = Column(Float)
    status = Column(String(50))
    employee_comment = Column(Text, nullable=True)
    manager_comment = Column(Text, nullable=True)
    goal_id = Column(Integer,ForeignKey("goals.id"))
    created_at = Column(DateTime,default=datetime.utcnow)