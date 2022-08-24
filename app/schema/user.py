from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
class UserResponse(UserBase):
    id: int