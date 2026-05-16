from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class CheckIn(Base):

    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    quarter = Column(String(10))
    progress = Column(Integer)
    remarks = Column(String(500))
    manager_feedback = Column(String(500), nullable=True)
    checkin_date = Column(String(50))
    status = Column(String(50), default="pending")
    
    goal_id = Column(Integer, ForeignKey("goals.id"))