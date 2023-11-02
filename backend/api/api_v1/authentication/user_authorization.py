from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from bson import ObjectId
from core.db.mongo import MongoDBManager
from core.hashing import Hasher
from core.config import config
from core.log import Logger
from api.api_v1.authentication import token as TokenManager

# def check_if_allowed():
#     return


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = TokenManager.Token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def verify_password(userdata: dict, requested_pw: str):
    hashed_pw = userdata["password"]
    result = Hasher.verify_password(
        password=requested_pw, stored_hash=hashed_pw
    )
    Logger.debug(f"verify_password resulkt: {result}")
    if not result:
        return False
    elif result:
        return True


async def authenticate_user(id: str, password: str) -> tuple[bool, dict]:
    mongo_manager = MongoDBManager(
        collection_name="Users",
        db_name=config.MongodbSettings.MONGODB_NAME,
        db_url=config.MongodbSettings.MONGODB_URL,
    )

    bool, user = await mongo_manager.read_manager.find_one(
        {"_id": ObjectId(id)}
    )

    if not user:
        return False, None
    if not await verify_password(userdata=user, requested_pw=password):
        return False, None
    return True, user
