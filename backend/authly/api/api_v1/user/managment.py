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


async def is_new_email_valid(
    email, read_manager: MongoDBManager.ReadManager
) -> bool:
    try:
        _, data = await read_manager.find_one({"email": str(email)})

    except FileNotFoundError as file:
        Logger.log(LogLevel.DEBUG, "email not registered", file)
        return False

    else:
        Logger.log(LogLevel.ERROR, "email in use:", data)
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

    if not await is_new_email_valid(email, mongo_client.read_manager):
        try:
            (
                _,
                edited_id,
            ) = await mongo_client.write_manager.insert_document(
                data=user_data_dict
            )
            Logger.log(LogLevel.ERROR, "mongo returned:", edited_id)

        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            )

        else:
            return {
                "user_id": str(edited_id),
                "username": username,
                "email": email,
            }
        finally:
            await mongo_client.close_connection()

    raise ValueError("Email In use or Blacklisted")


async def update_username(
    user_id: str, new_username, mongo_client: MongoDBManager
):
    try:
        (
            _,
            data,
        ) = await mongo_client.read_manager.find_one(
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
            await mongo_client.update_manager.update_one_document(
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
    try:
        (
            _,
            data,
        ) = await mongo_client.read_manager.find_one(
            query={"_id": ObjectId(user_id)}
        )
        Logger.log(
            LogLevel.DEBUG,
            f"user_id({user_id})",
            f"data({data})",
        )
    except FileNotFoundError:
        raise ValueError("user_id not found")

    except Exception as e:
        Logger.log(LogLevel.ERROR, f"unexpected exception {e}")
        raise Exception(f"unexpected exception {e}")

    else:
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
