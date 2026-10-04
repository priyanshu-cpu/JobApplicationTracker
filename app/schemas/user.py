from pydantic import BaseModel, Field, EmailStr, ConfigDict, PlainSerializer
from datetime import datetime
from typing import Annotated


FormattedDT = Annotated[
    datetime,
    PlainSerializer(lambda v: v.strftime("%Y-%m-%d %H:%M:%S"), return_type=str),
]



class User(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    created_at: FormattedDT
    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    message: str
    user: UserOut
