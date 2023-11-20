from datetime import datetime
from bson import ObjectId


from pydantic import EmailStr
from backend.authly.core.utils.object_id import (
    convert_object_id_to_str,
)
from backend.authly.core.db.mongo_crud import MongoDBManager
from backend.authly.config import application_config
from backend.authly.core.utils.log import Logger, LogLevel

mongo_config = application_config.MongodbSettings  # type: ignore


async def is_email_in_use(
    email, read_manager: MongoDBManager.ReadManager
) -> bool:
    status, data = await read_manager.find_one({"email": str(email)})
    if status:
        Logger.log(LogLevel.ERROR, "email in use:", data)
        return False
    return True


async def create_user(
    email: EmailStr, password: str, role: list, mongo_client: MongoDBManager
) -> dict:
    current_time = datetime.now().isoformat()
    username = email.split("@")[0]
    # Generate a unique user ID
    user_data_dict = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "disabled": False,
        "geo_location": "None",
        "username_history": [{username: {"from": current_time, "to": None}}],
        "email_history": [{email: {"from": current_time, "to": None}}],
        "keys": [],
    }

    if not await is_email_in_use(email, mongo_client.read_manager):
        (
            _,
            edited_id,
        ) = await mongo_client.write_manager.insert_document(
            data=user_data_dict
        )

        # TODO: add back email vlaidation

        Logger.log(LogLevel.ERROR, "mongo returned:", edited_id)

        await mongo_client.close_connection()
        return {
            "user_id": str(edited_id),
            "username": username,
            "email": email,
        }

    return False


async def delete_user_by_id(
    user_id: str, mongo_client: MongoDBManager
) -> tuple[bool, str]:
    (
        status,
        data,
    ) = await mongo_client.delete_manager.delete_document(
        query={"_id": ObjectId(user_id)}
    )

    return (status, data)


# reworked:
async def get_user_data_by_id(
    user_id: str, mongo_client: MongoDBManager
) -> dict:
    (
        status,
        data,
    ) = await mongo_client.read_manager.find_one(
        query={"_id": ObjectId(user_id)}
    )
    Logger.log(
        LogLevel.DEBUG,
        f"user_id({user_id})",
        f"data({data})",
    )

    return convert_object_id_to_str(data)


async def get_user_data_by_email(
    email: str, mongo_client: MongoDBManager
) -> tuple[bool, dict[str, str]]:
    (
        status,
        data,
    ) = await mongo_client.read_manager.find_one({"email": str(email)})
    Logger.log(
        LogLevel.DEBUG,
        "user data by email",
        f"status({status})",
        f"email({email})",
        f"data({data})",
    )
    return (status, convert_object_id_to_str(data))


async def get_user_data_by_username(
    username: str, mongo_client: MongoDBManager
) -> tuple[bool, dict[str, str]]:
    (
        status,
        data,
    ) = await mongo_client.read_manager.find_one(query={"username": username})
    Logger.log(
        LogLevel.DEBUG,
        "user data by email",
        f"status({status})",
        f"email({username})",
        f"data({data})",
    )
    return (status, convert_object_id_to_str(data))


# async def update_username(
#     user_id: str, new_username, mongo_client: MongoDBManager
# ):
#     try:
#         (
#             _,
#             data,
#         ) = await mongo_client.read_manager.find_one(
#             query={"_id": ObjectId(user_id)}
#         )

#         if data:
#             # Fetch the old username
#             old_username = data.get("username")
#             # Update the username in the fetched data
#             data["username"] = new_username

#             # Update the username history
#             current_time = datetime.now().isoformat()
#             for entry in data["username_history"]:
#                 if old_username in entry:
#                     entry[old_username]["to"] = current_time
#                     break

#             data["username_history"].append(
#                 {new_username: {"from": current_time, "to": None}}
#             )

#             # Update the document in the collection
#             await mongo_client.update_manager.update_one_document(
#                 {"_id": ObjectId(user_id)}, data
#             )

#             Logger.log(LogLevel.DEBUG, f"Updated user data: {data}")
#             return True, "Username updated successfully."
#         else:
#             Logger.log(LogLevel.DEBUG, f"No user found with ID: {user_id}")
#             return False, "User not found."
#     except Exception as e:
#         Logger.log(
#             LogLevel.DEBUG, f"Error occurred while updating username: {e}"
#         )
#         return (
#             False,
#             "Error occurred while updating username. read more in logs",
#         )
