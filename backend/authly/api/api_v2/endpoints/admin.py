from typing import Annotated
from authly.api.api_v2 import http_exceptions
from authly.core.utils.log import LogLevel, Logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from authly.crud import crud_admin
from authly.models import admin_model as core
from authly.api.api_v2.models import admin_model as admin_reponse
from authly.security.authentication import admin_auth

admin = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@admin.get("/")
async def admin_router_hello_world():
    return {"msg": "Hello World from admin endpoint"}


@admin.post("/", response_model=admin_reponse.CreateAdminReponse)
async def create_admin(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        success, result, details = await crud_admin.create_admin_account(
            core.CreateAdmin(
                password=user_data.password, email=user_data.username
            )
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Issues with the connection to the MongoDB server. "
                "Make sure to configure it correctly."
                f"details: {details}. ",
            )

    except HTTPException:
        raise
    else:
        return result


@admin.post("/token", response_model=admin_reponse.Token)
async def admin_login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        new_token = await admin_auth.authenticate_admin_user(user_data)

    except ValueError as e:
        Logger.log(LogLevel.ERROR, "ValueError:", e)
        raise http_exceptions.credentials_exception

    except ValidationException as e:
        Logger.log(LogLevel.ERROR, "ValidationException:", e)
        raise http_exceptions.credentials_exception

    except Exception as e:
        Logger.log(LogLevel.ERROR, "unknown Exception:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    else:
        return {
            "access_token": new_token,
            "token_type": "bearer",
        }


@admin.get("/me", response_model=admin_reponse.AdminAccount)
async def get_current_admin_user(
    current_user: Annotated[
        core.AdminAccount, Depends(admin_auth.get_current_admin_user)
    ]
):
    return current_user


@admin.get("/all", response_model=admin_reponse.AllAdminAccounts)
async def get_all_admin_accounts(
    current_user: Annotated[
        core.AdminAccount, Depends(admin_auth.get_current_admin_user)
    ]
):
    try:
        success, result, details = await crud_admin.get_admin_accounts()
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Issues with the connection to the MongoDB server. "
                "Make sure to configure it correctly."
                f"details: {details}. ",
            )

    except HTTPException:
        raise

    else:
        return result
    

@admin.post("/collection")
async def create_new_collection():
    
