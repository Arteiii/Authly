from datetime import datetime
from fastapi import HTTPException


from authly.core.utils.object_id import (
    convert_object_id_to_string,
    convert_object_id_to_str_dictionary,
)

from authly.db.mongo import MongoDBManager
from authly.core.config import application_config
from authly.core.utils.log import Logger, LogLevel
from authly.api.user import model as userModel


mongo_config = application_config.MongodbSettings  # type: ignore


async def is_new_email_valid(email, mongo_client: MongoDBManager) -> bool:
    try:
        success, data, _ = await mongo_client.find_one({"email": str(email)})

        if not success:
            return True

        return False

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Exception:", e)


async def create_user(
    email: str,
    password: str,
    mongo_client: MongoDBManager,
    role: list[userModel.UserRole] = [userModel.UserRole.USER],
) -> userModel.User:
    current_time = datetime.now().isoformat()
    username = email.split("@")[0]

    user_data = userModel.User(
        username=username,
        email=email,
        password=password,
        role=role,
        disabled=False,
        geo_location="",
        username_history=[
            userModel.UsernameHistoryEntry(from_date=current_time)
        ],
        email_history=[userModel.EmailHistoryEntry(from_date=current_time)],
    )

    if await is_new_email_valid(email, mongo_client):
        try:
            (
                _,
                edited_id,
                _,
            ) = await mongo_client.insert_document(data=user_data.model_dump())

            Logger.log(LogLevel.DEBUG, "mongo returned:", edited_id)

            user_data.id = convert_object_id_to_string(edited_id)

            Logger.log(LogLevel.DEBUG, user_data)

        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            )

        else:
            return user_data

    raise ValueError("Email In use or Blacklisted")


async def get_user_data_by_email(
    email: str, mongo_client: MongoDBManager
) -> tuple[bool, dict[str, str]]:
    (
        status,
        data,
    ) = await mongo_client.find_one({"email": str(email)})
    Logger.log(
        LogLevel.DEBUG,
        "user data by email",
        f"status({status})",
        f"email({email})",
        f"data({data})",
    )
    return (status, convert_object_id_to_str_dictionary(data))
