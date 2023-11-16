"""
main.py
"""
from typing import Annotated
from authly.api.api_v1.db.connect import get_mongo_manager, get_redis_manager
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from authly.api.api_v1.authentication import token as TokenManager
from authly.api.api_v1.authentication import (
    password_hashing as password_manager,
)
from authly.api.api_v1.authentication import user_authorization as ua
from authly.api.api_v1.user import managment
from authly.api.api_v1.model import model
from authly.api.api_v1 import exceptions
from authly.core.config import application_config
from authly.core.log import Logger, LogLevel
from pydantic import ValidationError

Mongo_URL = application_config.MongodbSettings.MONGODB_URL  # type: ignore

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")

UserCollectionName = "Users"


class MongoConfig:
    mongo_config = application_config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


class RedisConfig:
    redis_config = application_config.RedisdbSettings  # type: ignore
    db = redis_config.REDIS_DB
    host = redis_config.REDIS_HOST
    port = redis_config.REDIS_PORT


@app.get("/")
async def user_router_hello_world():
    return {"msg": "Hello World"}


@app.post("/")
async def register_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    ## Register a user. (V1)

    :param user_data: Data required for user registration.
    """

    try:
        hashed_password = await password_manager.hash_password(
            password=user_data.password
        )

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Exception while hashing password", f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        results = await managment.create_user(
            email=user_data.username,
            role=["User"],
            password=hashed_password,
            mongo_client=get_mongo_manager(UserCollectionName),
        )

    except ValueError as ve:
        Logger.log(LogLevel.ERROR, f"Bad Request: {ve}")
        return HTTPException(
            status_code=400, detail="Email In use or Blacklisted"
        )

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Exception while creating user", f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    else:
        return results


# add base 654 vlaidation for passwords
@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        mongo_manager = get_mongo_manager(UserCollectionName)
        user = await ua.authenticate_user(
            form_data.username, form_data.password, mongo_manager
        )
        Logger.log(LogLevel.DEBUG, user)

    except FileNotFoundError as e:
        Logger.log(
            LogLevel.ERROR, "email/user not found", "FileNotFoundError", e
        )
        raise exceptions.credentials_exception

    except ValidationError as e:
        Logger.log(LogLevel.ERROR, "password missmatch", "ValidationErr", e)
        raise exceptions.credentials_exception

    except Exception as e:
        Logger.log(LogLevel.ERROR, e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    else:
        redis_manager = get_redis_manager()
        redis_manager.connect()
        new_token = TokenManager.get_new_token(
            user_id=str(user.get("id")),
            expiration_time_minutes=240,
            redis_manager=redis_manager,
        )
        # close connections
        await mongo_manager.close_connection()
        redis_manager.close()
        Logger.log(LogLevel.DEBUG, "New token:", new_token)

        return {"access_token": new_token, "token_type": "bearer"}


@app.get("/me", response_model=None)  # , response_model=model.User
async def read_users_me(
    current_user: Annotated[dict, Depends(ua.get_current_user)]
):
    Logger.log(
        LogLevel.INFO, "users/me: (get('id'))", current_user.get("id")  # type: ignore
    )
    current_user.pop("password", None)

    return current_user


@app.post("/email")
async def update_email(
    update_email: model.UpdateUserEmail,
    current_user: Annotated[
        model.UpdateUserEmail, Depends(ua.get_current_user)
    ],
):
    return update_email.email
