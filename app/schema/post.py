from typing import List

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(None, name="title", description="Post title")
    description: str = Field(None, name="Description", description="Post details")


class Post(PostBase):
    id: int
    user_id: int
    likes_count: int = Field(0, name="Likes", description="Total no of likes")
    likes: List[str] = Field(
        [], name="Likes List", description="List of user IDs who liked the post"
    )

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    likes_count: int = Field(0, name="Likes", description="Total no of likes")

    class Config:
        from_attributes = True


class AllPostResponse(BaseModel):
    posts: List[PostResponse]
