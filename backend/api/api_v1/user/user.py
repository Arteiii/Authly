"""
main.py
"""
import time

from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

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


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def login_log_reponse(data) -> dict:
    return {
        "id": str(data["_id"]),
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


@app.post("/token")
async def login(form_data: Annotated[ua.OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    user = UserInDB(**user_dict)
    hashed_password = ua.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}


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
