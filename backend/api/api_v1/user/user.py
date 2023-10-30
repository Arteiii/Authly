"""
main.py
"""
import time

from typing import Annotated, Union

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


from api.api_v1.user import model
from core.config import config
from core.db.mongo import MongoDBManager
from core.hashing import Hasher


app = APIRouter()
Mongo_URL = config.MongodbSettings.MONGODB_URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# utils


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


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
    if config.Debug.DebugHashingTime is True:
        print(password)
        print(f"using: {config.PasswordConfig.HASHING_ALGORITHM}")
        start_time = time.time()  # Record the start time

    hashed = await Hasher.get_password_hash(password=password)

    end_time = time.time()  # Record the end time

    if config.Debug.DebugHashingTime is True:
        print("Hashed Password:", hashed)
        print("Hashing Time:", end_time - start_time, "seconds")

    return hashed


@app.post("/")
async def register_user(user_data: model.UserRegistration):
    """
    ## Register a user. (V1)


    :param email: user email

    :param username: The user's username. Username must consist of 3 letters,\
        a '#' character, and 4 numbers. (abc#1234)

    :param password: The user's password in Base64\
        must be at least 8 characters long and contain at\
            least one uppercase letter, one lowercase letter,\
                one digit, and one special character (e.g., @$!%*?&).
    """

    password = user_data.password

    # Convert the Pydantic model to a dictionary using dict()
    user_data_dict = user_data.dict()

    password_hashed = await hash_password(password=password)

    user_data_dict["password"] = password_hashed

    try:
        mongo_client = MongoDBManager(
            db_url=Mongo_URL, db_name="mydb", collection_name="Users"
        )

        # Insert the dictionary into the MongoDB collection
        result = await mongo_client.write_manager.insert_document(
            data=user_data_dict
        )

        return result

    finally:
        await mongo_client.close_connection()


@app.get("/", response_model=model.UserDataResponse)
async def get_users_by_username(data: model.GetUsersByName):
    """
    # Search for users by usernames. (V1)

    This endpoint takes a list of usernames and\
        returns user data for each username.

    Args:
        data (model.GetUsersByName):\
            Request data containing a list of usernames.

    Returns:
        dict: A dictionary with usernames as keys and user data as values.

    ### Example Request:
    ```json
    {
        "usernames": ["abc#1234", "abcasdasdc#1224"]
    }
    ```
    ### Example Response:
    ```json
    {
        "user_data": {
            "abc#1234": {
                "email": "user@example.com",
                "username": "abc#1234",
                "password": "$argon2id$..."
            },
            "abcasdasdc#1224": {
                "email": "user2@example.com",
                "username": "abcasdasdc#1224",
                "password": "$argon2id$..."
            }
        }
    }
    ```
    """
    usernames = data.usernames

    try:
        mongo_client = MongoDBManager(
            collection_name="Users",
            db_name="mydb",
            db_url=Mongo_URL,
        )

        response_data = {}  # Initialize an empty dictionary

        for username in usernames:
            search_dict = {"username": f"{username}"}
            print(search_dict)
            user_data = await mongo_client.read_manager.find_one(
                query=search_dict
            )

            if user_data:
                # Convert the ObjectId to a string
                user_data["_id"] = str(user_data["_id"])
                response_data[username] = {**user_data, "username": username}
            else:
                response_data[username] = None  # User not found

        return {"user_data": response_data}
    finally:
        await mongo_client.close_connection()


@app.post("/token")
async def login_for_access_token(
    request: Request, credentials: model.GetToken
):
    return "token"


@app.get("/login")
async def login_with_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
