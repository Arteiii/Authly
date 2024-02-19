from typing import Annotated
from fastapi import APIRouter, Depends

from authly.api.security.authentication import auth
from authly.api.user import model as userModel

user = APIRouter()


@user.get("/")
async def user_router_hello_world(Depends):
    return {
        "msg": f"Hello World from user Route",
        "name": "current_user",
    }


@user.get("/me")
async def get_current_admin_user(
    current_user: Annotated[userModel.User, Depends(auth.get_current_user_id)],
):
    return current_user
