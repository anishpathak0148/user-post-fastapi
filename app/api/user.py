from fastapi import APIRouter, status

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=status.HTTP_200_OK)
def get_all_users():
    return {"users": ["user1", "user2"]}