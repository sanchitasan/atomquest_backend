from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base


class Goal(Base):

    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(500))
    thrust_area = Column(String(255))
    uom = Column(String(50))
    target_value = Column(Integer)
    weightage = Column(Integer)
    status = Column(String(50), default="draft")
    is_locked = Column(Boolean, default=False)
    employee_id = Column(Integer,ForeignKey("users.id"))
    manager_id = Column(Integer,ForeignKey("users.id"),nullable=True)
    approved_by = Column(Integer,ForeignKey("users.id"),nullable=True)