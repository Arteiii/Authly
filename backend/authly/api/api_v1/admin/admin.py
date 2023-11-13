"""
main.py
"""
from fastapi import APIRouter

from backend.authly.core.db.mongo_crud import MongoDBManager
from authly.api.api_v1.admin import model as model
from authly.api.api_v1.admin.admin_account_managment import (
    create_admin as create,
)
from authly.core.config import application_config

Mongo_URL = application_config.MongodbSettings.MONGODB_URL  # type: ignore
Mongo_NAME = application_config.MongodbSettings.MONGODB_NAME  # type: ignore

app = APIRouter()


@app.post("/")
async def create_admin(user_data: model.AdminRegistration):
    mongo_client = MongoDBManager(Mongo_URL, Mongo_NAME, "ADMIN")
    (create_status, create_result) = await create.create_admin(
        user_data.username, user_data.email, user_data.password, mongo_client
    )
    (status, result, details) = await mongo_client.close_connection()

    return create_status, create_result


@app.post("/container")
async def create_container(user_data: model.AdminRegistration):
    mongo_client = MongoDBManager(Mongo_URL, Mongo_NAME, "ADMIN")
    (create_status, create_result) = await create.create_admin(
        user_data.username, user_data.email, user_data.password, mongo_client
    )
    (status, result, details) = await mongo_client.close_connection()

    return create_status, create_result
