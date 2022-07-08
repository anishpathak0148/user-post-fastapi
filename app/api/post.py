from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.get("",status_code= 200)
def get_all_posts():
    return {"post": "All post"}