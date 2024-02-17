from fastapi import APIRouter, Depends


user = APIRouter()


@user.get("/{bubble_id}")
async def user_router_hello_world():
    return {
        "msg": f"Hello World from user Route",
        "name": "current_user",
    }
