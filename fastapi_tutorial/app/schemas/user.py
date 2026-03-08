from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    roles: List[str] = []


class UserInDB(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserOut(UserBase):
    id: int
    roles: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
