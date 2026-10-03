from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ApplicationBase(BaseModel):
    company: str
    status: str
    job_title: str
    location: str
    salary: int
    applied_at: datetime | None = Field(default=datetime.now())
    notes: str | None = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    company: str
    status: str
    job_title: str
    location: str
    salary: int
    created_at: datetime
    applied_at: datetime | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ApplicatoinCreateResponse(BaseModel):
    message: str
    data : ApplicationOut