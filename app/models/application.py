from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    salary = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    applied_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="applications")
