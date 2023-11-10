from datetime import datetime
from typing import List
from bson import ObjectId
from email_validator import EmailNotValidError, validate_email


from pydantic import EmailStr
from backend.authly.core.object_id import (
    convert_object_id_to_str,
    convert_str_to_object_id,
)
from backend.authly.core.db.mongo_crud import MongoDBManager
from backend.authly.core.config import application_config
from backend.authly.core.log import Logger


class UserManagment:
    def __init__(
        self,
        collection: str = "Users",
        db_name: str = application_config.MongodbSettings.MONGODB_NAME,
        url: str = application_config.MongodbSettings.MONGODB_URL,
    ):
        self.mongo_client = MongoDBManager(
            collection_name=collection,
            db_name=db_name,
            db_url=url,
        )

    async def create_user(
        self, username: str, email: EmailStr, password: str, role: list | str
    ):
        current_time = datetime.now().isoformat()

        # Generate a unique user ID
        user_data_dict = {
            "username": username,
            "email": email,
            "password": password,
            "role": [role],
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

        (
            is_email_in_use,
            existing_user,
        ) = await self.mongo_client.read_manager.find_one(
            {"email": str(email)}
        )

        if is_email_in_use:
            Logger.log(LogLevel.ERROR, "alread registered email")
            return False, "alread registered email"

        # Insert the user data into the MongoDB collection
        (
            bool,
            edited_id,
        ) = await self.mongo_client.write_manager.insert_document(
            data=user_data_dict
        )
        if bool is not True:
            Logger.log(LogLevel.ERROR, f"mongo returned invalid op ({bool})")

        result = {
            "mongo_state": bool,
            "user_id": edited_id,
            "username": username,
            "email": email,
        }

        return True, result

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

                Logger.log(
                    LogLevel.DEBUG, f"Updated user data: {old_user_data}"
                )
                return True, "Username updated successfully."
            else:
                Logger.log(LogLevel.DEBUG, f"No user found with ID: {user_id}")
                return False, "User not found."
        except Exception as e:
            Logger.log(
                LogLevel.DEBUG, f"Error occurred while updating username: {e}"
            )
            return (
                False,
                "Error occurred while updating username. read more in logs",
            )

    async def update_email(self, user_id: str, new_email):
        try:
            validate_email(new_email)
        except EmailNotValidError:
            Logger.log(LogLevel.ERROR, f"Invalid email address ({new_email})")
            raise ValueError(f"Invalid email address ({new_email})")

        bool, user = await self.mongo_client.read_manager.find_one(
            query={"_id": user_id}
        )
        Logger.log(LogLevel.DEBUG, f"update username user return = {user}")
        return user

    async def delete_user(self, user_id: List[str]):
        results = {}
        for id in user_id:
            (
                bool,
                db_result,
            ) = await self.mongo_client.delete_manager.delete_document(
                query={"_id": ObjectId(id)}
            )
            results[id] = bool

        if False in results.values():
            return False, results
        else:
            return True, results

    async def update_user_roles(
        self,
        user_id: [str],
        add_roles: List = None,
        remove_roles: List = None,
        set_roles: List = None,
    ):
        results = {}

        op_result = "suc..."  # returns from mongo crud
        # after ops:
        results = {user_id: op_result}
        return results

    async def get_user_data(
        self, user_id: str = None, email: str = None, username: str = None
    ):
        # Check if at least one of the parameters is provided
        if not user_id and not email and not username:
            raise ValueError(
                "At least one of user_id, email, or username is required."
            )

        # Use a more efficient method to check which argument is provided
        if user_id:
            status, data = await self.mongo_client.read_manager.find_one(
                query={"_id": ObjectId(user_id)}
            )
            Logger.log(
                LogLevel.DEBUG,
                f"get_user_data - user_id (status): {status}",
                f"get_user_data - user_id (data): {data}",
            )
        if email:
            query = {"email": str(email)}
            status, data = await self.mongo_client.read_manager.find_one(query)
            Logger.log(
                LogLevel.DEBUG,
                f"email: {email}",
                f"get_user_data - email (status): {status}",
                f"get_user_data - email (data): {data}",
            )
        if username:
            status, data = await self.mongo_client.read_manager.find_one(
                query={"username": username}
            )
            Logger.log(
                LogLevel.DEBUG,
                f"get_user_data - username (status): {status}",
                f"get_user_data - username (data): {data}",
            )

        data = convert_object_id_to_str(data)

        Logger.log(
            LogLevel.DEBUG,
            "final output after convert_object_id_to_str (status)",
            f"{status}",
            "final output after convert_object_id_to_str (data)",
            f"{data}",
        )

        return status, data
