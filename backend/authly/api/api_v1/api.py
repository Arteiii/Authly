from authly.api.api_v1.user.user import app as user
from authly.api.api_v1.key.api import app as key
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user, prefix="/user")
api_router.include_router(key, prefix="/key")
