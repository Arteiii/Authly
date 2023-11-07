from backend.authly.api.api_v1.key.generation import generate_keys_with_format
from backend.authly.core.db.mongo import MongoDBManager
from backend.authly.core.config import config
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


async def delete_key(
    keys: list = None, creators: list = None, applications: list = None
):
    try:
        if not any([keys, creators, applications]):
            raise ValueError(
                "Please provide keys, creators, or application IDs."
            )

        mongo_manager = MongoDBManager(
            db_url=config.MongodbSettings.MONGODB_URL,
            db_name=config.MongodbSettings.MONGODB_NAME,
            collection_name="Keys",
        )

        delete_manager = mongo_manager.DeleteManager(
            collection=mongo_manager.collection
        )

        results = {}
        if keys:
            for key in keys:
                delete_query = {"key_value": key}
                delete_key = await delete_manager.delete_many_documents(
                    query=delete_query
                )
                results[key] = delete_key

        if creators:
            for creator in creators:
                delete_query = {"creator": creator}
                delete_creator = await delete_manager.delete_many_documents(
                    query=delete_query
                )
                results[creator] = delete_creator

        if applications:
            for app_id in applications:
                delete_query = {"application_id": app_id}
                delete_result = await delete_manager.delete_many_documents(
                    query=delete_query
                )
                results[app_id] = delete_result

        print(results)
        return results  # Assuming successful deletion

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        await mongo_manager.close_connection()
