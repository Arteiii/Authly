from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from authly.crud import crud_admin
from authly.models import admin_crud_model
from authly.api.api_v2.models import admin_model


app = APIRouter()


@app.get("/")
async def admin_router_hello_world():
    return {"msg": "Hello World from admin endpoint"}


@app.put("/", response_model=admin_model.CreateAdminReponse)
async def create_admin(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    await crud_admin.create_admin_account(
        admin_crud_model.CreateAdmin(
            password=user_data.password, email=user_data.username
        )
    )
