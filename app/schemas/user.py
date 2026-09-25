from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    email : str | None = Field(default=None)

class UserOut(BaseModel):
    id: int
    username:str
    email:str

