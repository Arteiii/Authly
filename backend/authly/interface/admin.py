from authly.db.mongo import MongoDBManager
from authly.models import admin_crud_model
from authly.core.utils.log import Logger, LogLevel


async def insert_admin_user(
    data: admin_crud_model.AdminAccount,
) -> admin_crud_model.AdminAccount:
    try:
        mongo_manager: MongoDBManager = MongoDBManager("Admin")
        _, data.id, details = await mongo_manager.insert_document(
            {
                "username": data.username,
                "password": data.password,
                "email": data.email,
                "container": data.container,
                "settings": data.settings,
            }
        )
        Logger.log(LogLevel.DEBUG, details)
    except Exception as e:
        Logger.log(LogLevel.ERROR, "Error occured in interface/admin:", e)
        raise Exception(e)

    else:
        return data
