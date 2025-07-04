# THIRDPARTY
from pydantic import BaseModel, EmailStr, Field


class SUsersAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=15)


class SUsers(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_admin: bool
