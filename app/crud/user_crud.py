from asyncio.log import logger
from sqlalchemy.orm import Session
from app import models
from app.schema import user as user_schema


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def get_user_by_email(db: Session, email: str):
    user =  db.query(models.User).filter(models.User.email == email).first()
    return user


def get_users(db: Session, offset: int = 0, limit: int = 100):
    users =  db.query(models.User).offset(offset).limit(limit).all()
    logger.info(f"Users from crud operation: {users}")
    return users


def create_user(db: Session, user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(name = user.name, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: user_schema.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user