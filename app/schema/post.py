from typing import List
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str = Field(None, name="title", description="Post title")
    description: str = Field(None, name="Description", description="Post details")
    likes: int = Field(0, name="Likes", description="Total no of likes")


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True


class AllPostResponse(BaseModel):
    posts: List[PostResponse]