from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from authly.crud import crud_admin
from authly.models import admin_model as core
from authly.api.api_v2.models import admin_model as reponse_model


admin = APIRouter()


@admin.get("/")
async def admin_router_hello_world():
    return {"msg": "Hello World from admin endpoint"}


@admin.put("/")
async def create_admin(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    await crud_admin.create_admin_account(
        core.CreateAdmin(password=user_data.password, email=user_data.username)
    )
