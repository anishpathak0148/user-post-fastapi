from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TEXT
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


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True,)
    description = Column(TEXT)
    likes = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("user_table.id"))
    
    owner = relationship("User", back_populates="posts")