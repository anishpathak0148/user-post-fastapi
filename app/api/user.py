from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import user_crud
from app.schema import user as user_schema
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "", 
    status_code=status.HTTP_200_OK,
    response_model= List[user_schema.User]
)
def get_all_users(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = user_crud.get_users(db, offset=offset, limit=limit)
    print(f"User list is: {users}")
    return users


@router.get(
    "/id",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.User
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):
    user = user_crud.get_user(db, user_id=id)
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)



@router.put("/id", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
def update_user_details(
    id: int,
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    db_user = user_crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user_crud.update_user(db=db, user_id=id, user=user)