"""
main.py
"""
import time
import json

from typing import List
from fastapi import APIRouter, Query, FastAPI, HTTPException
from bson import ObjectId

from api.api_v1.user import model
from core.hashing import Hasher
from core.db.mongo import MongoDBClient
from core.config import config


# utils


def hash_password(password) -> str:
    if config.Debug.DebugHashingTime is True:
        print(password)
        print(f"using: {config.PasswordConfig.HASHING_ALGORITHM}")
        start_time = time.time()  # Record the start time

    hashed = Hasher.get_password_hash(password=password)

    end_time = time.time()  # Record the end time

    if config.Debug.DebugHashingTime is True:
        print("Hashed Password:", hashed)
        print("Hashing Time:", end_time - start_time, "seconds")

    return hashed


app = APIRouter()


@app.post("/register")
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
    user_data_dict = dict(user_data)

    password_hashed = hash_password(password=password)

    user_data_dict["password"] = password_hashed

    try:
        mongo_client = MongoDBClient()

        # Insert the dictionary into the MongoDB collection
        result = await mongo_client.insert_document(
            collection_name="Users",
            document=user_data_dict,
        )
        return result

    finally:
        await mongo_client.close()


@app.get("/get_users_by_name", response_model=model.UserDataResponse)
async def get_users_by_name(data: model.GetUsersByName):
    """
    # Get user data by usernames.

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
        mongo_client = MongoDBClient()

        response_data = {}  # Initialize an empty dictionary

        for username in usernames:
            search_dict = {"username": username}
            user_data = await mongo_client.find_document_by_dict(
                collection_name="Users", search=search_dict
            )

            if user_data:
                # Convert the ObjectId to a string
                user_data["_id"] = str(user_data["_id"])
                response_data[username] = {**user_data, "username": username}
            else:
                response_data[username] = None  # User not found

        return {"user_data": response_data}
    finally:
        await mongo_client.close()


# @app.post("/token")
# async def login_for_access_token():
