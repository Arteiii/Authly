from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
)  # , OAuth2PasswordRequestForm

from authly.core.db.mongo_crud import MongoDBManager
from authly.core.db.redis_crud import RedisManager
from authly.core.hashing import Hasher
from authly.core.config import application_config
from authly.core.log import Logger, LogLevel
from authly.api.api_v1.authentication import token as TokenManager
from authly.api.api_v1.user.managment import UserManagment
import authly.api.api_v1.user.model as UserModel
from authly.core.object_id import convert_object_id_to_str


redis_config = application_config.RedisdbSettings  # type: ignore
redis_db = redis_config.REDIS_DB
redis_host = redis_config.REDIS_HOST
redis_port = redis_config.REDIS_PORT


class MongoConfig:
    mongo_config = application_config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


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


async def get_current_active_user(
    current_user: Annotated[UserModel.User, Depends(get_current_user)]
):
    if current_user.get("disabled"):  # type: ignore
        Logger.log(
            LogLevel.ERROR, "error curretn user inactive:", f"{current_user}"
        )
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def verify_password(userdata: dict, requested_pw: str):
    hashed_pw = userdata["password"]
    result = Hasher.verify_password(
        password=requested_pw, stored_hash=hashed_pw
    )
    Logger.log(LogLevel.DEBUG, f"verify_password result: {result}")
    if not result:
        return False
    elif result:
        return True


async def authenticate_user(email: str, password: str) -> tuple[bool, dict]:
    mongo_manager = MongoDBManager(
        collection_name="Users",
        db_name=MongoConfig.name,
        db_url=MongoConfig.url,
    )

    status, user, details = await mongo_manager.read_manager.find_one(
        {"email": email}
    )
    user = convert_object_id_to_str(user)

    if not user:
        return (
            False,
            {"message": "user empty"},
        )
    if not await verify_password(userdata=user, requested_pw=password):
        Logger.log(LogLevel.ERROR, )
        return (
            False,
            {"message": "operation failed"},
        )
    return True, user
