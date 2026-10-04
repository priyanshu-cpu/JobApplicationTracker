from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    location = Column(String, index=True)
    salary = Column(Integer)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now(), nullable=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="applications")
