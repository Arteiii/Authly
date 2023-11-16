from backend.authly.core.db.mongo_crud import MongoDBManager
from backend.authly.api.api_v1.authentication import (
    password_hashing as password_manager,
)
from backend.authly.core.log import Logger, LogLevel


# async def create_admin(
#     username: str,
#     email: str,
#     password: str,
#     mongo_client: MongoDBManager,
# ) -> tuple[bool, dict]:
#     user_data_dict = {
#         "username": username,
#         "email": email,
#         "password": password_manager.hash_password(password),
#         "role": ["admin"],
#         "contianers": [],
#     }

#     (
#         email_in_use,
#         existing_user,
#         details,
#     ) = await mongo_client.read_manager.find_one({"email": str(email)})

#     if email_in_use:
#         Logger.log(LogLevel.ERROR, "alread registered email")
#         return (False, "Invalid email address")

#     # Insert the user data into the MongoDB collection
#     (
#         status,
#         edited_id,
#         details,
#     ) = await mongo_client.write_manager.insert_document(data=user_data_dict)
#     if status is not True:
#         Logger.log(LogLevel.ERROR, f"mongo returned invalid op ({status})")

#     result = {
#         "mongo_state": status,
#         "user_id": edited_id,
#         "username": username,
#         "email": email,
#     }

#     return (True, result)
