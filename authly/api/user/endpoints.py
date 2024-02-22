from typing import Annotated

import fastapi
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError


from authly.api.security.authentication import auth
from authly.api.user import model as userModel
from authly.api.user import user as userManager

from authly.core.utils.log import Logger, LogLevel
from authly.api.security.authentication import token_module as TokenManager
from authly.db.mongo import MongoDBManager
from authly.db.redis import RedisManager

user = APIRouter()


@user.get("/")
async def user_router_hello_world(Depends):
    return {
        "msg": f"Hello World from user Route",
        "name": "current_user",
    }


@user.get("/me")
async def get_current_user(
    current_user: Annotated[userModel.User, Depends(auth.get_current_user_id)],
):
    return current_user


@user.post("/", response_model=userModel.CreateUserResponse)
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> userModel.CreateUserResponse:
    try:
        mongo_client = MongoDBManager("user")

        data = await userManager.create_user(
            email=str(form_data.username),
            password=str(form_data.password),
            mongo_client=mongo_client,
            role=[userModel.UserRole.USER],
        )

        Logger.log(LogLevel.DEBUG, data)

        return userModel.CreateUserResponse(
            id=data.id, username=data.username, email=data.email
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )  # Return a 400 Bad Request with the error message

    except ValidationError as e:
        raise HTTPException(
            status_code=422, detail=e.errors()
        )  # Return a 422 Unprocessable Entity with the validation errors

    finally:
        (
            success,
            results,
            status,
        ) = await mongo_client.close_connection()

        if not success:
            Logger.log(
                LogLevel.ERROR,
                f"close_connection failed: ",
                success,
                results,
                status,
            )


@user.post("/token", response_model=auth.TokenModel)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> auth.TokenModel:
    try:
        mongo_client = MongoDBManager("user")

        token = await auth.authenticate_user(form_data, mongo_client)

        Logger.log(LogLevel.DEBUG, user)

    except FileNotFoundError as e:
        Logger.log(
            LogLevel.ERROR, "email/user not found", "FileNotFoundError", e
        )
        raise HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="email/user not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # modify if you want to exclude specific infos

    except ValidationError as e:
        Logger.log(LogLevel.ERROR, "password missmatch", "ValidationErr", e)
        raise HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="password missmatch",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # modify if you want to exclude specific infos

    except Exception as e:
        Logger.log(LogLevel.ERROR, e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    else:
        return token

    finally:
        (
            success,
            results,
            status,
        ) = await mongo_client.close_connection()

        if not success:
            Logger.log(
                LogLevel.ERROR,
                f"close_connection failed: ",
                success,
                results,
                status,
            )
