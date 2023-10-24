from fastapi import APIRouter

from api.api_v1.user.user import app as user

api_router = APIRouter()


@api_router.get("/")
async def helloworld() -> str:
    return "Hello World! from api v1"


api_router.include_router(user, prefix="/user")
