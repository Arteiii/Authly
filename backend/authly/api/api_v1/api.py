from authly.api.api_v1.user.user import app as user
from authly.api.api_v1.admin.admin import app as admin
from fastapi import APIRouter

api_router = APIRouter()

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
        "The **login** logic is also here.",
    },
    {
        "name": "admin",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/",
        },
    },
]

api_router.include_router(user, tags=["users"], prefix="/user")
api_router.include_router(admin, tags=["admin"], prefix="/admin")


@api_router.get("/")
async def api_router_hello_world():
    return {"msg": "Hello World"}
