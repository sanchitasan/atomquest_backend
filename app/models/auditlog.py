from sqlalchemy import Column, Integer, String
from app.database import Base

class AuditLog(Base):

    __tablename__ = "auditlogs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255))
    performed_by = Column(String(100))
    role = Column(String(50))
    entity = Column(String(100))
