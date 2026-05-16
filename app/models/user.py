from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50))
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(String(50))
    updated_at = Column(String(50))