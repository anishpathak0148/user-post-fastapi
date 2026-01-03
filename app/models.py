from sqlalchemy import TEXT, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="owner")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
        }


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String,
        unique=True,
        index=True,
    )
    description = Column(TEXT)
    likes_count = Column(Integer, default=0)

    # Store list as a JSON string using a custom type
    likes = Column(MutableList.as_mutable(JSON), default=list)

    user_id = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="posts")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "likes_count": self.likes_count,
            "likes": self.likes,
            "user_id": self.user_id,
        }
