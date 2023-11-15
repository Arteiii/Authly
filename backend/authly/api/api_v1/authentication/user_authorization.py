from typing import Annotated
from authly.api.api_v1.db.connect import get_mongo_manager

from fastapi import Depends, HTTPException
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

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


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
    try:
        user_id = TokenManager.get_user_id(token)

    except Exception:
        raise credentials_exception

    else:
        return await get_user_data(user_id)


async def authenticate_user(
    email: str, password: str, mongo_manager: MongoDBManager
) -> dict:
    try:
        _, user = await mongo_manager.read_manager.find_one({"email": email})

    except FileNotFoundError as e:
        Logger.log(LogLevel.ERROR, "error in authenticate_user:", "except:", e)
        raise HTTPException(status_code=500, detail="email not found")

    else:
        stored_hash = user["password"]
        user = convert_object_id_to_str(user)
        if await password_manager.verify_password(password, stored_hash):
            return user

        raise HTTPException(status_code=500, detail="password missmatch")
