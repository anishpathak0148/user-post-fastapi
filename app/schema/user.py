from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., title="Name of the user", max_length=100)
    email: str = Field(..., title="Email address of the user", max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., title="Password for the user", min_length=6)


class User(UserBase):
    id: int = Field(..., title="ID of the user")
    role: str = Field(
        default="user", title="Role of the user", description="Can be 'user' or 'admin'"
    )
    is_active: bool = Field(default=True, title="Is the user active?")

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int = Field(..., title="ID of the user")
    is_active: bool = Field(default=True, title="Is the user active?")
