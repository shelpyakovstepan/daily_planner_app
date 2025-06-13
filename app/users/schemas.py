from pydantic import BaseModel, EmailStr


class SUsersAuth(BaseModel):
    email: EmailStr
    password: str


class SUsers(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_admin: bool
