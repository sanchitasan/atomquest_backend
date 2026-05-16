from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(500))
    trust_area = Column(String(255))
    uom = Column(String(50))
    target_value = Column(Integer)
    weightage = Column(Integer)
    status = Column(String(50), default="pending")
    created_at = Column(String(50))
    updated_at = Column(String(50))
    start_date = Column(String(50))
    end_date = Column(String(50))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_date = Column(String(50), nullable=True)
    employee_id = Column(Integer, ForeignKey("users.id"))