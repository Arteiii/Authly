import random

from typing import List
from email_validator import EmailNotValidError, validate_email


from pydantic import EmailStr
from core.db.mongo import MongoDBManager
from core.config import config
from core.log import Logger


class UserManagment:
    def __init__(
        self,
        collection: str = "Users",
        db_name: str = "UserData",
        url: str = config.MongodbSettings.MONGODB_URL,
    ):
        self.mongo_client = MongoDBManager(
            collection_name=collection,
            db_name=db_name,
            db_url=url,
        )

    async def gen_user_id(self) -> int:
        while True:
            user_id = random.randint(0, 9999999999)
            if not await self.is_user_id(user_id):
                return user_id

    async def is_user_id(self, id: int) -> bool:
        result, msg = await self.mongo_client.read_manager.find_one(
            {"user_id": id}
        )
        Logger.debug(f"result fo uid search in db: {msg}")
        return result

    async def create_user(
        self, username: str, email: EmailStr, password: str, role: str
    ) -> dict:
        # Generate a unique user ID
        user_id = await self.gen_user_id()

        user_data_dict = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password": password,
            "role": role,
            "disabled": False,
            "geo_location": "None",
            "keys": [],
        }

        # Check if email is valid
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email address")

        # Insert the user data into the MongoDB collection
        mongo_results = await self.mongo_client.write_manager.insert_document(
            data=user_data_dict
        )

        result = {
            "mongo_results": mongo_results,
            "user_id": user_id,
            "username": username,
            "email": email,
        }

        return result

    async def update_username(self, user_id: int, new_username):
        # add source
        return new_username

    async def delete_user(self, user_id: List[int]):
        db_result = "succe.."  # add logic
        results = {user_id: db_result}
        return results

    async def update_user_roles(
        self,
        user_id: [int],
        add_roles: List = None,
        remove_roles: List = None,
        set_roles: List = None,
    ):
        results = {}

        op_result = "suc..."  # returns from mongo crud
        # after ops:
        results = {user_id: op_result}
        return results
