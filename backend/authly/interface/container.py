from typing import Tuple
from authly.db.mongo import MongoDBManager
from authly.core.utils.log import Logger, LogLevel
from authly.models import container_model, user_model
from bson import InvalidDocument, ObjectId


async def create_container_in_collection(
    collection: str,
    config: user_model.UserDB,
) -> str:
    mongo_manager = MongoDBManager(collection)
    try:
        status, data, details = await mongo_manager.insert_document(
            {
                "container_id": config.container_id,
                "container_name": config.container_name,
            }
        )
        Logger.log(
            LogLevel.DEBUG,
            "create_container_in_collections:",
            status,
            data,
            details,
        )
    except Exception:
        raise

    else:
        return str(data)

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise


async def create_container_config(
    collection_name,
    config: container_model.ContainerConfig,
) -> Tuple[bool, str]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        status, data, details = await mongo_manager.insert_document(
            config.dict()
        )
        Logger.log(
            LogLevel.DEBUG,
            "create_container_in_collections:",
            status,
            data,
            details,
        )
        new_document_id = str(data)

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, new_document_id


async def update_container_config(
    collection_name,
    config: container_model.ContainerConfig,
) -> Tuple[bool, str]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        status, data, details = await mongo_manager.update_one_document(
            query={"_id": ObjectId(config.id)}, update_data=config.dict()
        )
        Logger.log(
            LogLevel.DEBUG,
            "update_container_config:",
            status,
            data,
            details,
        )
        new_document_id = str(data)

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, new_document_id


async def get_container_data(
    collection_name: str,
    container_id: ObjectId,
) -> Tuple[bool, container_model.ContainerConfig]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        status, data, details = await mongo_manager.find_one(
            {"_id": container_id}
        )
        Logger.log(
            LogLevel.DEBUG,
            "get_container_data:",
            status,
            data,
            details,
        )
        if not data:
            raise Exception(f"invalid data: ({data})")
    except InvalidDocument:
        raise

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, container_model.ContainerConfig(**data)
