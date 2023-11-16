from typing import Annotated
from xml.dom import ValidationErr
from authly.api.api_v1 import exceptions
from authly.api.api_v1.db.connect import get_mongo_manager, get_redis_manager
from authly.core.db.redis_crud import RedisManager

from fastapi import Depends, HTTPException
from fastapi.exceptions import ValidationException
from fastapi.security import (
    OAuth2PasswordBearer,
)  # , OAuth2PasswordRequestForm

from authly.core.db.mongo_crud import MongoDBManager
from authly.core.log import Logger, LogLevel
from authly.api.api_v1.authentication import token as TokenManager
from authly.api.api_v1.authentication import (
    password_hashing as password_manager,
)
from authly.api.api_v1.user import managment
from authly.core.object_id import convert_object_id_to_str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


async def get_user_data(user_id: str) -> dict:
    try:
        data = await managment.get_user_data_by_id(
            user_id, get_mongo_manager("Users")
        )
    except ValueError as e:
        Logger.log(LogLevel.ERROR, "ValueError in get_current_user:", e)
        raise HTTPException(status_code=500, detail="internal server issues")

    except Exception as e:
        Logger.log(LogLevel.ERROR, "error in get_current_user:", e)
        raise HTTPException(status_code=500, detail="internal server issues")

    else:
        return dict(data)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    redis_manager = get_redis_manager()
    try:
        redis_manager.connect()
        user_id = TokenManager.get_user_id(token, redis_manager)

    except Exception:
        raise exceptions.credentials_exception

    else:
        return await get_user_data(user_id)

    finally:
        redis_manager.close()


async def authenticate_user(
    email: str, password: str, mongo_manager: MongoDBManager
) -> dict:
    try:
        _, user = await mongo_manager.read_manager.find_one({"email": email})

    except FileNotFoundError as e:
        Logger.log(LogLevel.ERROR, "error in authenticate_user:", "except:", e)
        raise FileNotFoundError("email not found")

    else:
        stored_hash = user["password"]
        user = convert_object_id_to_str(user)
        try:
            await password_manager.verify_password(password, stored_hash)

        except ValidationException:
            raise ValidationErr("password missmatch")

        else:
            return user
