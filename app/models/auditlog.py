from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class AuditLog(Base):

    __tablename__ = "auditlogs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255))
    performed_by = Column(String(100))
    entity = Column(String(100))
    entity_id = Column(Integer, nullable=True)
    role = Column(String(100), nullable=True)
    employee_email = Column(String(100), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime,default=datetime.utcnow)