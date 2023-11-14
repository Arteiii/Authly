from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException


from pydantic import EmailStr
from backend.authly.core.object_id import (
    convert_object_id_to_str,
)
from backend.authly.core.db.mongo_crud import MongoDBManager
from backend.authly.core.config import application_config
from backend.authly.core.log import Logger, LogLevel

mongo_config = application_config.MongodbSettings  # type: ignore


class UserManagment:
    def __init__(
        self,
        collection: str = "Users",
        db_name: str = mongo_config.MONGODB_NAME,
        url: str = mongo_config.MONGODB_URL,
    ):
        self.mongo_client = MongoDBManager(
            collection_name=collection,
            db_name=db_name,
            db_url=url,
        )

    async def create_user(
        self, email: EmailStr, password: str, role: list | str
    ) -> dict:
        current_time = datetime.now().isoformat()
        username = email.split("@")[0]
        # Generate a unique user ID
        user_data_dict = {
            "username": username,
            "email": email,
            "password": password,
            "role": [role],
            "disabled": False,
            "geo_location": "None",
            "username_history": [{email: {"from": current_time, "to": None}}],
            "email_history": [{email: {"from": current_time, "to": None}}],
            "keys": [],
        }

        try:
            email_in_use, _ = await self.mongo_client.read_manager.find_one(
                {"email": str(email)}
            )
        except FileNotFoundError:
            Logger.log(LogLevel.ERROR, "alread registered email")
            raise ValueError("Email In use or Blacklisted")

        try:
            # Insert the user data into the MongoDB collection
            (
                _,
                edited_id,
            ) = await self.mongo_client.write_manager.insert_document(
                data=user_data_dict
            )
            Logger.log(
                LogLevel.ERROR, f"mongo returned invalid op ({edited_id})"
            )

        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            )

        else:
            return {
                "user_id": edited_id,
                "username": username,
                "email": email,
            }

    async def update_username(self, user_id: str, new_username):
        try:
            (
                _,
                data,
            ) = await self.mongo_client.read_manager.find_one(
                query={"_id": ObjectId(user_id)}
            )

            if data:
                # Fetch the old username
                old_username = data.get("username")
                # Update the username in the fetched data
                data["username"] = new_username

                # Update the username history
                current_time = datetime.now().isoformat()
                for entry in data["username_history"]:
                    if old_username in entry:
                        entry[old_username]["to"] = current_time
                        break

                data["username_history"].append(
                    {new_username: {"from": current_time, "to": None}}
                )

                # Update the document in the collection
                await self.mongo_client.update_manager.update_one_document(
                    {"_id": ObjectId(user_id)}, data
                )

                Logger.log(LogLevel.DEBUG, f"Updated user data: {data}")
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

    async def delete_user_by_id(self, user_id: str) -> tuple[bool, str]:
        (
            status,
            data,
        ) = await self.mongo_client.delete_manager.delete_document(
            query={"_id": ObjectId(user_id)}
        )

        return (status, data)

    # reworked:
    async def get_user_data_by_id(
        self, user_id: str
    ) -> tuple[bool, dict[str, str]]:
        (
            status,
            data,
        ) = await self.mongo_client.read_manager.find_one(
            query={"_id": ObjectId(user_id)}
        )
        Logger.log(
            LogLevel.DEBUG,
            f"user data by id status({status})",
            f"user_id({user_id})",
            f"data({data})",
        )
        return (status, convert_object_id_to_str(data))

    async def get_user_data_by_email(
        self, email: str
    ) -> tuple[bool, dict[str, str]]:
        (
            status,
            data,
        ) = await self.mongo_client.read_manager.find_one(
            {"email": str(email)}
        )
        Logger.log(
            LogLevel.DEBUG,
            "user data by email",
            f"status({status})",
            f"email({email})",
            f"data({data})",
        )
        return (status, convert_object_id_to_str(data))

    async def get_user_data_by_username(
        self, username: str
    ) -> tuple[bool, dict[str, str]]:
        (
            status,
            data,
        ) = await self.mongo_client.read_manager.find_one(
            query={"username": username}
        )
        Logger.log(
            LogLevel.DEBUG,
            "user data by email",
            f"status({status})",
            f"email({username})",
            f"data({data})",
        )
        return (status, convert_object_id_to_str(data))
