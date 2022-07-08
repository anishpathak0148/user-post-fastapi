from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=200)
def get_all_users():
    return {"users": ["user1", "user2"]}