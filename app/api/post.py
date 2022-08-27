from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.auth import get_current_active_user
from app.crud import post_crud
from app.crud import user_crud
from app.schema.user import User

from app.schema.post import Post, PostResponse, PostBase, AllPostResponse

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "",
    status_code= status.HTTP_200_OK,
    response_model= AllPostResponse,
    description="Get All post"
)
def get_all_posts(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    posts = post_crud.get_posts(db=db, limit=limit, offset=offset)
    return {"posts": posts}


@router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model= Post,
    description="Get post by id"
)
def get_post(
    id: int,
    db: Session = Depends(get_db)
):
    post_data = post_crud.get_post_by_id(db, id)
    if post_data is None:
        raise HTTPException(
            status_code=404,
            detail = f"Post with id: {id} not found."
        )
    return post_data

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model= PostResponse,
    description="Create Post"
)
def create_post(
    payload: PostBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user_id = current_user.id
    user_data = user_crud.get_user(db=db, user_id=user_id)
    if user_data is None:
        raise HTTPException(
            status_code=400,
            detail=f"Bad Request! User with user id: {user_id} not exist."
        )
    post_data = post_crud.create_user_post(db=db, post=payload, user_id=user_id)
    return post_data


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
    description="Update post details"
)
def update_post(
    id: int,
    payload: PostBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    post_data = post_crud.get_post_by_id(db, id)
    if post_data is None:
        raise HTTPException(
            status_code=404,
            detail = f"Post with id: {id} not found."
        )
    updated_post = post_crud.update_post(db=db, id=id, post=payload)
    return updated_post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # response_model="",
    description="delete post"
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    post_data = post_crud.get_post_by_id(db, id)
    if post_data is None:
        raise HTTPException(
            status_code=404,
            detail = f"Post with id: {id} not found."
        )
    return post_crud.delete_post(db=db, id=id)