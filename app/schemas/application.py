from pydantic import BaseModel, Field
from datetime import datetime

class Application(BaseModel):
    company :str
    status:str
    job_title:str
    location:str
    salary:str
    applied_at: datetime |None = Field(default=datetime.now())
    notes:str | None = Field(default=None)

class ApplicationOut(BaseModel):
    id: int
    user_id :int
    company :str
    status:str
    job_title:str
    location:str
    salary:str
    created_at: datetime
    applied_at: datetime
    notes:str | None = Field(default=None)
