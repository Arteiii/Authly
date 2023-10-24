from api.api_v1.user.user import app as user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user, prefix="/user")
