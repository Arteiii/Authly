from typing import Annotated, Any, Tuple

from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
)  # , OAuth2PasswordRequestForm

from authly.core.db.mongo_crud import MongoDBManager
from authly.core.db.redis_crud import RedisManager
from authly.core.log import Logger, LogLevel
from authly.core.config import application_config
from authly.api.api_v1.authentication import token as TokenManager
from authly.api.api_v1.authentication import (
    password_hashing as password_manager,
)
from authly.api.api_v1.user.managment import UserManagment
from authly.core.object_id import convert_object_id_to_str


redis_config = application_config.RedisdbSettings  # type: ignore
redis_db = redis_config.REDIS_DB
redis_host = redis_config.REDIS_HOST
redis_port = redis_config.REDIS_PORT


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    redis_manager = RedisManager(redis_port, redis_db, redis_host)

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    (status_bool, user_id, details) = TokenManager.get_user_id(
        token, redis_manager
    )

    if status_bool is False:
        raise credentials_exception
    if user_id is None:
        raise credentials_exception
    user_manager = UserManagment()

    status, data = await user_manager.get_user_data_by_id(user_id)
    if status is False:
        Logger.log(
            LogLevel.ERROR,
            "error in get_current_user:",
            f"status({status})",
            f"data({data})",
        )
        raise HTTPException(status_code=500, detail="internal server issues")
    return data


async def authenticate_user(
    email: str, password: str, mongo_manager: MongoDBManager
) -> dict:
    try:
        _, user = await mongo_manager.read_manager.find_one({"email": email})

    except FileNotFoundError as e:
        Logger.log(LogLevel.ERROR, "error in authenticate_user:", "except:", e)
        raise HTTPException(status_code=500, detail="email not found")

    else:
        user = convert_object_id_to_str(user)
        if await password_manager.verify_password(user, password):
            return user

        raise HTTPException(status_code=500, detail="password missmatch")
