from fastapi import APIRouter


user = APIRouter()


@user.get("/")
async def user_router_hello_world():
    return {"msg": "Hello World from user endpoint"}
