import asyncio
from datetime import datetime
from authly.core.db.mongo import MongoDBManager
from authly.core.config import config
from authly.core.log import Logger

MONGODB_URL = config.MongodbSettings.MONGODB_URL
DB_NAME = f"{config.MongodbSettings.MONGODB_NAME}TESTER"
COLLECTION_NAME = "Test"


# Create an instance of the MongoDBManager
mongo = MongoDBManager(
    db_url=MONGODB_URL, db_name=DB_NAME, collection_name=COLLECTION_NAME
)


# Test function to check the MongoDB operations
async def async_mongo_operations():
    test_results = {"TEST_TITLE": "MongoDB"}

    # Connect to MongoDB
    connected = await mongo.client.server_info()
    if connected:
        test_results["connection"] = "Passed"
    if not connected:
        Logger.critical("Failed to connect to MongoDB:", connected)
        return test_results

    # Perform a write operation
    data = {"example_key": "example_value", "timestamp": datetime.now()}
    _, inserted_id = await mongo.write_manager.insert_document(data)
    if _:
        test_results["write_operation"] = "Passed"
        Logger.debug(f"Document inserted with ID: {inserted_id}")
    else:
        test_results["write_operation"] = "Failed"
        Logger.error("Failed to insert document into MongoDB")

    # Perform a read operation
    query = {"example_key": "example_value"}
    _, result = await mongo.read_manager.find_one(query)
    if _:
        test_results["read_operation"] = "Passed"
        Logger.debug(f"Document retrieved from MongoDB: {result}")
    else:
        test_results["read_operation"] = "Failed"
        Logger.error("Failed to retrieve document from MongoDB")

    # Perform an update operation
    update_data = {"set": {"example_key": "updated_value"}}
    _, update_result = await mongo.update_manager.update_one_document(
        query, update_data
    )
    if _:
        test_results["update_operation"] = "Passed"
        Logger.debug("Document updated successfully in MongoDB")
    else:
        test_results["update_operation"] = "Failed"
        Logger.error("Failed to update document in MongoDB")

    # Perform a delete operation
    _, delete_result = await mongo.delete_manager.delete_document(query)
    if _:
        test_results["delete_operation"] = "Passed"
        Logger.debug("Document deleted successfully from MongoDB")
    else:
        test_results["delete_operation"] = "Failed"
        Logger.error("Failed to delete document from MongoDB")

    try:
        await mongo.client.drop_database(DB_NAME)
        Logger.debug(f"The database '{DB_NAME}' has been deleted")
    except Exception as e:
        Logger.error(f"Failed to delete the database '{DB_NAME}': {e}")

    # Close the MongoDB connection
    closed, _ = await mongo.close_connection()
    if closed:
        test_results["close_connection"] = "Passed"
        Logger.debug("MongoDB connection closed successfully")
    else:
        test_results["close_connection"] = "Failed"
        Logger.error("Failed to close MongoDB connection")

    return test_results


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_mongo_operations())
