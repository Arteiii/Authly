import random


from datetime import datetime
from typing import List
from bson import ObjectId
from email_validator import EmailNotValidError, validate_email


from pydantic import EmailStr
from core.db.mongo import MongoDBManager
from core.config import config
from core.log import Logger


class UserManagment:
    def __init__(
        self,
        collection: str = "Users",
        db_name: str = config.MongodbSettings.MONGODB_NAME,
        url: str = config.MongodbSettings.MONGODB_URL,
    ):
        self.mongo_client = MongoDBManager(
            collection_name=collection,
            db_name=db_name,
            db_url=url,
        )

    async def create_user(
        self, username: str, email: EmailStr, password: str, role: str
    ) -> dict:
        current_time = datetime.now().isoformat()

        # Generate a unique user ID
        user_data_dict = {
            "username": username,
            "email": email,
            "password": password,
            "role": role,
            "disabled": False,
            "geo_location": "None",
            "username_history": [
                {username: {"from": current_time, "to": None}}
            ],
            "email_history": [{email: {"from": current_time, "to": None}}],
            "keys": [],
        }

        # Check if email is valid
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email address")

        # Insert the user data into the MongoDB collection
        (
            bool,
            edited_id,
        ) = await self.mongo_client.write_manager.insert_document(
            data=user_data_dict
        )
        if bool is not True:
            Logger.error(f"mongo returned invalid op ({bool})")

        result = {
            "mongo_state": bool,
            "user_id": edited_id,
            "username": username,
            "email": email,
        }

        return result

    async def update_username(self, user_id: str, new_username):
        try:
            (
                bool_find_one_result,
                old_user_data,
            ) = await self.mongo_client.read_manager.find_one(
                query={"_id": ObjectId(user_id)}
            )

            if old_user_data:
                # Fetch the old username
                old_username = old_user_data.get("username")

                # Update the username in the fetched data
                old_user_data["username"] = new_username

                # Update the username history
                current_time = datetime.now().isoformat()
                for entry in old_user_data["username_history"]:
                    if old_username in entry:
                        entry[old_username]["to"] = current_time
                        break

                old_user_data["username_history"].append(
                    {new_username: {"from": current_time, "to": None}}
                )

                # Update the document in the collection
                await self.mongo_client.update_manager.update_one_document(
                    {"_id": ObjectId(user_id)}, old_user_data
                )

                Logger.debug(f"Updated user data: {old_user_data}")
                return True, "Username updated successfully."
            else:
                Logger.debug(f"No user found with ID: {user_id}")
                return False, "User not found."
        except Exception as e:
            Logger.debug(f"Error occurred while updating username: {e}")
            return False, f"Error occurred while updating username: {e}"

    async def update_email(self, user_id: int, new_email):
        try:
            validate_email(new_email)
        except EmailNotValidError:
            Logger.error(f"Invalid email address ({new_email})")
            raise ValueError(f"Invalid email address ({new_email})")

        user = await self.mongo_client.read_manager.find_one(
            query={"user_id": user_id}
        )
        Logger.debug(f"update username user return = {user}")

        return user

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
