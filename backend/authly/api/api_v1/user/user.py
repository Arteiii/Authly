"""
main.py
"""
from typing import Annotated
from authly.core.db.mongo_crud import MongoDBManager
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from authly.api.api_v1.authentication import token as TokenManager
from authly.api.api_v1.authentication import (
    password_hashing as password_manager,
)
from authly.api.api_v1.authentication import user_authorization as ua
from authly.api.api_v1.user.managment import UserManagment
from authly.api.api_v1.user import model
from authly.core.config import application_config
from authly.core.log import Logger, LogLevel
from authly.core.db.redis_crud import RedisManager

Mongo_URL = application_config.MongodbSettings.MONGODB_URL  # type: ignore

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


class MongoConfig:
    mongo_config = application_config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


class RedisConfig:
    redis_config = application_config.RedisdbSettings  # type: ignore
    db = redis_config.REDIS_DB
    host = redis_config.REDIS_HOST
    port = redis_config.REDIS_PORT


# def login_log_reponse(data) -> dict:
#     return {
#         "_id": str(data["_id"]),
#         "ip_address": data["ip_address"],
#         "password": data["password"],
#         "username": data["username"],
#         "event_type": data["event_type"],
#         "status": data["status"],
#         "session_duration_minutes": data["session_duration_minutes"],
#         "additional_info": data["additional_info"],
#         "url": data["url"],
#         "method": data["method"],
#         "headers": data["headers"],
#         "body": data["body"],
#         "timestamp": data["timestamp"],
#     }


@app.post("/")
async def register_user(user_data: model.UserRegistration):
    """
    ## Register a user. (V1)

    :param user_data: Data required for user registration.
    """
    try:
        user_manager = UserManagment()

        hashed_password = await password_manager.hash_password(
            password=user_data.password
        )

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Exception while hashing password", f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        result_bool, results = await user_manager.create_user(
            username=user_data.username,
            email=user_data.email,
            role="User",
            password=hashed_password,
        )

    except ValueError as ve:
        Logger.log(LogLevel.ERROR, f"Bad Request: {ve}")
        raise HTTPException(status_code=400, detail="Bad Request")

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Exception while creating user", f"{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if result_bool:
        return results
    elif not result_bool:
        raise HTTPException(
            status_code=500, detail="Email In use or Blacklisted"
        )


@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    mongo_manager = MongoDBManager(
        collection_name="Users",
        db_name=MongoConfig.name,
        db_url=MongoConfig.url,
    )
    (valid, user) = await ua.authenticate_user(
        form_data.username, form_data.password, mongo_manager
    )
    Logger.log(LogLevel.DEBUG, valid, user)
    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    redis_manager = RedisManager(
        RedisConfig.port, RedisConfig.db, RedisConfig.host
    )

    (status, data, details) = redis_manager.connect()
    Logger.log(
        LogLevel.DEBUG,
        f"status({status})",
        f"data({data})",
        f"details({details})",
    )
    status, new_token, details = TokenManager.get_new_token(
        user_id=str(user.get("id")),
        redis_manager=redis_manager,
        expiration_time_minutes=240,
    )
    # close connections
    redis_manager.close()
    mongo_manager.close_connection()
    Logger.log(
        LogLevel.DEBUG,
        f"status({status})",
        f"data({data})",
        f"details({details})",
    )
    if not status:
        Logger.log(
            LogLevel.ERROR,
            "Exception while creating token",
            f"{status}({new_token})",
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
    Logger.log(LogLevel.DEBUG, "New token:", new_token)
    return {"access_token": new_token, "token_type": "bearer"}


@app.get("/users/me", response_model=None)  # , response_model=model.User
async def read_users_me(
    current_user: Annotated[model.User, Depends(ua.get_current_user)]
):
    Logger.log(LogLevel.INFO, "users/me: (get('id'))", current_user.get("id"))

    return "Hello world"


@app.post("/emal")
async def update_email(
    update_email: model.UpdateUserEmail,
    current_user: Annotated[
        model.UpdateUserEmail, Depends(ua.get_current_user)
    ],
):
    return update_email.email
