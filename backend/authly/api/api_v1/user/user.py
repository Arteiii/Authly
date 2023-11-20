"""
main.py
"""
from typing import Annotated
from authly.api.api_v1.db import connect
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from authly.api.api_v1.authentication import token_module as TokenManager

from authly.api.api_v1.authentication import user_authorization as ua
from authly.api.api_v1.user import managment
from authly.api.api_v1.model import model
from authly.api.api_v1 import exceptions
from authly.core.utils import hashing, log
from authly import config
from pydantic import ValidationError

config = config.application_config
Mongo_URL = config.MongodbSettings.MONGODB_URL  # type: ignore

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")

UserCollectionName = "Users"


def return_new_token(user_id):
    redis_manager = connect.get_redis_manager()
    redis_manager.connect()
    return TokenManager.get_new_token(user_id, redis_manager)


class MongoConfig:
    mongo_config = config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


class RedisConfig:
    redis_config = config.RedisdbSettings  # type: ignore
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
        hashed_password = hashing.get_password_hash(user_data.password)

    except Exception as e:
        log.Logger.log(
            log.LogLevel.ERROR, "Exception while hashing password", f"{e}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        results = await managment.create_user(
            email=user_data.username,
            role=["User"],
            password=hashed_password,
            mongo_client=connect.get_mongo_manager(UserCollectionName),
        )

    except ValueError as ve:
        log.Logger.log(log.LogLevel.ERROR, f"Bad Request: {ve}")
        return HTTPException(
            status_code=400, detail="Email In use or Blacklisted"
        )

    except Exception as e:
        log.Logger.log(
            log.LogLevel.ERROR, "Exception while creating user", f"{e}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")

    else:
        return results


@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    mongo_manager = connect.get_mongo_manager(UserCollectionName)
    try:
        user = await ua.authenticate_user(
            form_data.username, form_data.password, mongo_manager
        )
        log.Logger.log(log.LogLevel.DEBUG, user)

    except FileNotFoundError:
        raise exceptions.credentials_exception

    except ValidationError:
        raise exceptions.credentials_exception

    except Exception as e:
        log.Logger.log(log.LogLevel.ERROR, e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    else:
        return {
            "access_token": return_new_token(str(user.get("id"))),
            "token_type": "bearer",
        }

    finally:
        await mongo_manager.close_connection()


@app.get("/me", response_model=None)  # , response_model=model.User
async def read_users_me(
    current_user: Annotated[dict, Depends(ua.get_current_user)]
):
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
