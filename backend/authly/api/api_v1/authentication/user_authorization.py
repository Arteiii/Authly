from typing import Annotated
from xml.dom import ValidationErr
from authly.api.api_v1 import exceptions
from authly.api.api_v1.db import connect

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from authly.db.mongo import MongoDBManager
from authly.core.utils.log import Logger, LogLevel
from authly.api.api_v1.authentication import token_module as TokenManager
from authly.api.api_v1.user import managment
from authly.core.utils.object_id import convert_object_id_to_str
from authly.core.utils import hashing


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    redis_manager = connect.get_redis_manager()
    try:
        redis_manager.connect()
        user_id = TokenManager.get_user_id(token, redis_manager)

    except Exception:
        raise exceptions.credentials_exception

    else:
        return await managment.get_user_data_by_id(
            user_id, connect.get_mongo_manager("Users")
        )

    finally:
        redis_manager.close()


async def authenticate_user(
    email: str, password: str, mongo_manager: MongoDBManager
) -> dict:
    try:
        _, user, _ = await mongo_manager.find_one({"email": email})

    except FileNotFoundError as e:
        Logger.log(LogLevel.ERROR, "error in authenticate_user:", "except:", e)
        raise FileNotFoundError("email not found")

    else:
        stored_hash = user["password"]
        user = convert_object_id_to_str(user)

        if hashing.verify_password(password, stored_hash):
            return user

        raise ValidationErr("password missmatch")
