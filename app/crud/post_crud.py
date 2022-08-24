from sqlalchemy.orm import Session
from app import models
from app.schema import post as post_schema


def get_posts(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Post).offset(offset).limit(limit).all()


def get_post_by_id(db: Session, id: int):
    post_details = db.query(models.Post).filter(models.Post.id == id).first()
    return post_details

def create_user_post(db: Session, post: post_schema.PostBase, user_id: int):
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: post_schema.PostBase, id: int):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    db_post.title = post.title
    db_post.description = post.description
    db_post.likes = post.likes

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, id: int):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(db_post)
    db.commit()
    return None
