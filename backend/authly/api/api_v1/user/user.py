"""
main.py
"""
import time

from typing import Annotated  # , Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from pydantic import BaseModel, EmailStr, ValidationError, validate_email

from authly.api.api_v1.authentication import token as token
from authly.api.api_v1.authentication import user_authorization as ua
from authly.api.api_v1.user import model
from authly.core.config import application_config
from authly.core.hashing import Hasher
from authly.api.api_v1.user.managment import UserManagment
from authly.core.log import Logger
from authly.core.log import LogLevel

app = APIRouter()
Mongo_URL = application_config.MongodbSettings.MONGODB_URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


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
    start_time = time.time()  # Record the start time

    hashed = Hasher.get_password_hash(password=password)

    end_time = time.time()  # Record the end time

    Logger.log(
        LogLevel.DEBUG,
        f"using: {application_config.PasswordConfig.HASHING_ALGORITHM}",
        f"Hashed Password: {hashed}",
        f"Hashing Time: {end_time - start_time} seconds",
    )

    return hashed


@app.post("/")
async def register_user(user_data: model.UserRegistration):
    """
    ## Register a user. (V1)

    :param user_data: Data required for user registration.
    """
    try:
        user_manager = UserManagment()

        hashed_password = await hash_password(password=user_data.password)

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

    finally:
        if result_bool:
            return results
        elif not result_bool:
            raise HTTPException(
                status_code=422, detail="Email In use or Blacklisted"
            )


@app.delete("/")
async def delete_user(data: model.DeleteUser) -> model.DeleteUserResponse:
    user_manager = UserManagment()

    is_success, results = await user_manager.delete_user(user_id=data.user_id)

    response = model.DeleteUserResponse(
        overall_status=is_success, details=[results]
    )

    if not is_success:
        Logger.log(
            LogLevel.DEBUG, "delete_user", f"{is_success}", f"{response}"
        )
    else:
        Logger.log(
            LogLevel.DEBUG, f"{is_success}", f"{response}", f"{type(response)}"
        )
    return response


@app.post("/token", response_model=model.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    (valid, user) = await ua.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _, new_token = token.Token(user_id=user.get("id"))
    if not _:
        Logger.log(
            LogLevel.ERROR,
            "Exception while creating token",
            f"{_}({new_token})",
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
    Logger.log(LogLevel.DEBUG, "New token:", new_token)
    return {"access_token": new_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=model.User)
async def read_users_me(
    current_user: Annotated[model.User, Depends(ua.get_current_active_user)]
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
#         Logger.log(LogLevel.ERROR, f"Exception while creating user ({e})")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
