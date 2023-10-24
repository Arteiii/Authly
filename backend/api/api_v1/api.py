from fastapi import APIRouter

from api.api_v1.user.user import app as user

api_router = APIRouter()

api_router.include_router(user, prefix="/user")
