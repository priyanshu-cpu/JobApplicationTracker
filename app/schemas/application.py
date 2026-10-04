from pydantic import BaseModel, Field, ConfigDict, PlainSerializer
from datetime import datetime, UTC
from typing import Annotated


FormattedDT = Annotated[
    datetime,
    PlainSerializer(lambda v: v.strftime("%Y-%m-%d %H:%M:%S"), return_type=str),
]



class ApplicationBase(BaseModel):
    company: str
    status: str
    job_title: str
    location: str
    salary: int
    applied_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))
    notes: str | None = None
    


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    company: str
    status: str
    job_title: str
    location: str
    salary: int
    created_at: FormattedDT
    applied_at: FormattedDT | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)



class ApplicationCreateResponse(BaseModel):
    message: str
    data : ApplicationOut



class ApplicationUpdate(BaseModel):
    status: str
    updated_at: datetime | None = None



class ApplicationOutUpdated(BaseModel):
    id: int
    user_id: int
    company: str
    status: str
    job_title: str
    location: str
    salary: int
    created_at: FormattedDT
    applied_at: FormattedDT | None = None
    updated_at: FormattedDT | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdateResponse(BaseModel):
    message: str
    data : ApplicationOutUpdated
