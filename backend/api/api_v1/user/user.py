"""
main.py
"""
import time

from typing import Annotated, Union
from email_validator import EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, ValidationError, validate_email

from api.api_v1.authentication import token as token
from api.api_v1.authentication import user_authorization as ua
from api.api_v1.user import model
from core.config import config
from core.db.mongo import MongoDBManager
from core.hashing import Hasher
from api.api_v1.user.managment import UserManagment
from core.log import Logger


app = APIRouter()
Mongo_URL = config.MongodbSettings.MONGODB_URL

# to get a string like this run:
# openssl rand -hex 32
# ef803e1df378a4a455844cfefb374da56f0e7c69de72c5190f67423b1edd4932


class User(BaseModel):
    username: str
    email: Union[EmailStr, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    _id: str
    password: str
    role: Union[str, None] = None
    geo_location: Union[str, None] = None


def login_log_reponse(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "ip_address": data["ip_address"],
        "password": data["password"],
        "username": data["username"],
        "event_type": data["event_type"],
        "status": data["status"],
        "session_duration_minutes": data["session_duration_minutes"],
        "additional_info": data["additional_info"],
        "url": data["url"],
        "method": data["method"],
        "headers": data["headers"],
        "body": data["body"],
        "timestamp": data["timestamp"],
    }


async def hash_password(password) -> str:
    Logger.debug(f"using: {config.PasswordConfig.HASHING_ALGORITHM}")
    start_time = time.time()  # Record the start time

    hashed = Hasher.get_password_hash(password=password)

    end_time = time.time()  # Record the end time

    Logger.debug(f"Hashed Password: {hashed}")
    Logger.debug(f"Hashing Time: {end_time - start_time} seconds")

    return hashed


@app.post("/")
async def register_user(user_data: model.UserRegistration) -> model.UserResult:
    """
    ## Register a user. (V1)

    :param user_data: Data required for user registration.
    """
    try:
        user_manager = UserManagment()

        hashed_password = await hash_password(password=user_data.password)
        results = await user_manager.create_user(
            username=user_data.username,
            email=user_data.email,
            role="User",
            password=hashed_password,
        )
        Logger.debug(results)
        return results

    except ValueError as ve:
        Logger.error(f"Bad Request: {ve}")
        raise HTTPException(status_code=400, detail="Bad Request")

    except Exception as e:
        Logger.error(f"Exception while creating user ({e})")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/")
async def delete_user(data: model.DeleteUser) -> model.DeleteUserResponse:
    user_manager = UserManagment()

    is_success, results = await user_manager.delete_user(user_id=data.user_id)

    response = model.DeleteUserResponse(
        overall_status=is_success, details=[results]
    )

    if not is_success:
        Logger.debug(
            f"""{__file__}, "delete_user", {is_success}, {response}"""
        )
    else:
        Logger.debug(f"""{is_success}, {response} {type(response)}""")
    return response


@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[ua.OAuth2PasswordRequestForm, Depends()]):
    user_manager = UserManagment()
    bool, user_dict = await user_manager.get_user_data(
        email=form_data.password
    )

    if not bool:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )

    user = UserInDB(**user_dict)
    Logger.debug(f"user.password: {user.password}")
    Logger.debug(f"user._id: {user._id}")
    pw_verify = Hasher.verify_password(
        password=form_data.password, hashed_password=user.password
    )

    if not pw_verify:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    else:
        access_token = token.Token(user_id=user._id)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=ua.User)
async def read_users_me(
    current_user: Annotated[str, Depends(ua.get_current_active_user)]
):
    return current_user


# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


# @app.patch("update_username")
# async def update_username(
#     data: model.UpdateUsername, token: Annotated[str, Depends(oauth2_scheme)]
# ):
#     try:
#         user_manager = UserManagment()

#         bool, results = await user_manager.update_username(
#             user_id=data.user_id,
#             new_username=data.username,
#         )
#         if bool is True:
#             return "Finished"
#         else:
#             raise HTTPException(
#                 status_code=500, detail="Internal Server Error"
#             )

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=f"Bad Request: {ve}")

#     except Exception as e:
#         Logger.error(f"Exception while creating user ({e})")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
