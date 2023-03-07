from fastapi import APIRouter
from starlette import status

router = APIRouter(tags=["Users"])


@router.get("/users")
def get_users():
    return []
