from api.api_v1.key.generation import generate_keys_with_format
from core.db.mongo import MongoDBManager
from core.config import config
import datetime


async def generate_new_key(
    duration, application_id, key_format, creator, num_keys=1
):
    generated_keys = await generate_keys_with_format(
        key_format=key_format, num_keys=num_keys
    )
    db_status = []

    try:
        mongo_manager = MongoDBManager(
            db_url=config.MongodbSettings.MONGODB_URL,
            db_name=config.MongodbSettings.MONGODB_NAME,
            collection_name="Keys",
        )

        write_manager = mongo_manager.WriteManager(
            collection=mongo_manager.collection
        )  # Pass the collection object

        for key in generated_keys:
            key_data = {
                "key_value": key,
                "creation_date": datetime.datetime.now(),
                "duration": duration,
                "application_id": application_id,
                "creator": creator,
            }
            # Store key data in MongoDB
            status = await write_manager.insert_document(
                data=key_data
            )  # Pass the document as a list
            db_status.append(status)

        return generated_keys

    finally:
        await mongo_manager.close_connection()


async def delete_key(application=None, creator=None, key=None):
    try:
        mongo_manager = MongoDBManager(
            db_url=config.MongodbSettings.MONGODB_URL,
            db_name=config.MongodbSettings.MONGODB_NAME,
            collection_name="Keys",
        )
<<<<<<< HEAD
=======
        db_status = {}

        read_manager = mongo_manager.ReadManager(
            collection=mongo_manager.collection
        )
>>>>>>> apirouting

        delete_manager = mongo_manager.DeleteManager(
            collection=mongo_manager.collection
        )

        delete_query = {}
        if application:
            delete_query = {"application_id": application}
        elif creator:
            delete_query = {"creator": creator}
        elif key:
            delete_query = {"key_value": key}

        elif not any([application, creator, key]):
            raise ValueError(
                "Please provide either application, creator, or key."
            )
        result = await delete_manager.delete_many_documents(query=delete_query)

        return result

    finally:
        await mongo_manager.close_connection()
