from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str


class UserCreated(BaseModel):
    user: UserOut
    detail: str = "User successfully created"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
