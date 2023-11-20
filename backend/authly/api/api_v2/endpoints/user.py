from fastapi import APIRouter


app = APIRouter()


@app.get("/")
async def user_router_hello_world():
    return {"msg": "Hello World from user endpoint"}
