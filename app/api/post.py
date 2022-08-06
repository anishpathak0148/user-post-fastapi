from fastapi import APIRouter, HTTPException

from app.schema.post import PostResponse, PostBase, AllPostResponse

post_data = {
    "posts": [
        {
            "id": 1,
            "title": "Post1",
            "description": "",
            "likes": 0
        },
        {
            "id": 2,
            "title": "Post2",
            "description": "",
            "likes": 0
        }
    ]
}

def find_post(id: int):
    for post in post_data["posts"]:
        if post["id"] == id:
            return post
    return None

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "",
    status_code= 200,
    response_model= AllPostResponse,
    description="Get All post"
)
def get_all_posts():
    return {"posts": post_data["posts"]}


@router.get(
    "/{id}", 
    status_code=200,
    response_model= PostResponse,
    description="Get post by id"
)
def get_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=404,
            detail = f"Post with id: {id} not found."
        )
    return post

@router.post(
    "",
    status_code=201,
    response_model= PostResponse,
    description="Create Post"
)
def create_post(
    payload: PostBase
):
    pass


@router.put(
    "/{id}",
    status_code=201,
    response_model=PostResponse,
    description="Update post details"
)
def update_post(
    id: int,
    payload: PostBase
):
    pass


@router.delete(
    "/{id}",
    status_code=204,
    response_model="",
    description="delete post"
)
def delete_post(
    id: int
):
    pass