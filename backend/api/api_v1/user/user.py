"""
main.py
"""
import time
from fastapi import APIRouter


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


@app.get("/hello")
async def hello() -> str:
    return "hello from users"


@app.post("/register")
def register_user(user_data: model.UserRegistration):
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

    mongo_client = MongoDBClient()

    # Insert the dictionary into the MongoDB collection
    result = mongo_client.insert_document(
        collection_name="Users",
        document=user_data_dict,
    )

    if Hasher.verify_password(password=password, stored_hash=password_hashed):
        return {
            "message": "User registered successfully",
            "DB": f"{result}",
        }
