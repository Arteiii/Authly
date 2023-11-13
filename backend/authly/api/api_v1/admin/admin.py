"""
main.py
"""
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException


from authly.core.db.mongo_crud import MongoDBManager
from authly.api.api_v1.admin import model as model
from authly.api.api_v1.admin.admin_account_managment import (
    create_admin as create,
)

from authly.api.api_v1.authentication import token as TokenManager
from authly.core.config import application_config
from authly.core.log import LogLevel, Logger
from authly.api.api_v1.authentication import user_authorization as ua
from authly.core.db.redis_crud import RedisManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/admin/token")


class MongoConfig:
    mongo_config = application_config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


class RedisConfig:
    redis_config = application_config.RedisdbSettings  # type: ignore
    db = redis_config.REDIS_DB
    host = redis_config.REDIS_HOST
    port = redis_config.REDIS_PORT


app = APIRouter()


def get_mongo_manager(
    db_url: str = MongoConfig.url,
    db_name: str = MongoConfig.name,
    collection_name: str = "ADMIN",
) -> MongoDBManager:
    return MongoDBManager(db_url, db_name, collection_name)


@app.post("/")
async def create_admin(user_data: model.AdminRegistration):
    mongo_manager = get_mongo_manager()
    (create_status, create_result) = await create.create_admin(
        user_data.username, user_data.email, user_data.password, mongo_manager
    )
    (status, result, details) = await mongo_manager.close_connection()

    return create_status, create_result


@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    mongo_manager = get_mongo_manager()
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
