from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    message: str
    user: UserOut
