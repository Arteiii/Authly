"""
Module for managing asynchronous MongoDB operations.

This module provides a MongoDBManager class that facilitates asynchronous\
    operations for creating, reading, updating, and deleting data in a\
        MongoDB database. It uses the motor library for asynchronous\
                interaction with MongoDB.

Classes:
- MongoDBManager: A class for managing asynchronous MongoDB operations\
    including Write, read, update, and delete operations.

Subclasses:
- WriteManager: A class for handling asynchronous creation operations.
- ReadManager: A class for handling asynchronous read operations.
- UpdateManager: A class for handling asynchronous update operations.
- DeleteManager: A class for handling asynchronous delete operations.

operations are named after the crud operations documentation from mongo:
https://www.mongodb.com/docs/manual/crud/

Author: Arteii/wavy42
Date: 25/10/2023
"""

import motor.motor_asyncio
import asyncio
from core.log import Logger


class MongoDBManager:
    def __init__(
        self,
        db_url,
        db_name,
        collection_name,
    ):
        """
        Initialize the MongoDBManager class.

        Args:
            db_url (str): The URL of the MongoDB database.
            db_name (str): The name of the MongoDB database.
            collection_name (str): The name of the MongoDB collection.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.update_manager = self.UpdateManager(self.collection)
        self.write_manager = self.WriteManager(self.collection)
        self.delete_manager = self.DeleteManager(self.collection)
        self.read_manager = self.ReadManager(self.collection)

    #####################################
    #               Write:             #
    #####################################

    class WriteManager:
        def __init__(self, collection):
            self.collection = collection

        async def insert_document(self, data):
            try:
                result = await self.collection.insert_one(data)
                inserted_id = str(result.inserted_id)
                Logger.debug(
                    f"Document with ID {inserted_id} inserted successfully"
                )
                return True, inserted_id
            except Exception as e:
                Logger.debug("Error occurred while inserting document", f"{e}")
                return False, "Error occurred while inserting document"

        async def insert_many_documents(self, data_list):
            try:
                await self.collection.insert_many(data_list)
                Logger.debug(
                    "Documents inserted successfully:", f"{data_list}"
                )
                return True, "Documents inserted successfully"
            except Exception as e:
                Logger.debug(
                    "Error occurred while inserting documents:", f"{e}"
                )
                return False, "Error occurred while inserting documents"

    #####################################
    #                Read:              #
    #####################################

    class ReadManager:
        def __init__(self, collection):
            self.collection = collection

        async def find_one(self, query):
            try:
                result = await self.collection.find_one(query)
                if result:
                    Logger.debug("Document found", f"{result}")
                    return True, result
                else:
                    Logger.debug("No document found with the given query")
                    return False, result
            except Exception as e:
                Logger.error(
                    "Error occurred during find_one operation", f"{e}"
                )
                return False, "Error occurred during find_one operation"

        async def find_many(self, query):
            try:
                result_list = []
                async for doc in self.collection.find(query):
                    result_list.append(doc)
                    Logger.debug("find many", f"{doc}")
                return True, result_list
            except Exception as e:
                Logger.error(
                    "Error occurred during find_many operation", f"{e}"
                )
                return False, "Error occurred during find_many operation"

    #####################################
    #               Update:             #
    #####################################

    class UpdateManager:
        def __init__(self, collection):
            self.collection = collection

        async def update_one_document(self, query, update_data):
            try:
                result = await self.collection.update_one(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    Logger.debug("Document updated successfully")
                    return True, "Document updated successfully"
                else:
                    Logger.debug("No document found with the given query")
                    return False, "No document found with the given query"
            except Exception as e:
                Logger.error(
                    "Error occurred during update_one operation", f"{e}"
                )
                return (
                    False,
                    "Error occurred during update_one operation",
                )

        async def update_many_documents(self, query, update_data):
            try:
                result = await self.collection.update_many(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    Logger.debug("Documents updated successfully")
                    return True, "Documents updated successfully"
                else:
                    Logger.debug("No document found with the given query")
                    return False, "No document found with the given query"
            except Exception as e:
                Logger.error(
                    "Error occurred during update_many operation", f"{e}"
                )
                return (
                    False,
                    "Error occurred during update_many operation",
                )

        async def replace_one_document(self, query, replace_data):
            try:
                result = await self.collection.replace_one(query, replace_data)
                if result.modified_count > 0:
                    Logger.debug("Document replaced successfully")
                    return True, "Document replaced successfully"
                else:
                    Logger.debug("No document found with the given query")
                    return False, "No document found with the given query"
            except Exception as e:
                Logger.error(
                    "Error occurred during replace_one operation", f"{e}"
                )
                return (
                    False,
                    "Error occurred during replace_one operation",
                )

    #####################################
    #               Delete:             #
    #####################################
    class DeleteManager:
        def __init__(self, collection):
            self.collection = collection

        async def delete_document(self, query):
            try:
                result = await self.collection.delete_one(query)
                if result.deleted_count > 0:
                    Logger.debug("Document deleted successfully")
                    return True, "Document deleted successfully"
                else:
                    Logger.debug("No document found with the given query")
                    return False, "No document found with the given query"
            except Exception as e:
                Logger.error(
                    "Error occurred during delete_document operation", f"{e}"
                )
                return (
                    False,
                    "Error occurred during delete_document operation",
                )

        async def delete_many_documents(self, query):
            try:
                result = await self.collection.delete_many(query)
                if result.deleted_count > 0:
                    Logger.debug("Documents deleted successfully")
                    return True, "Documents deleted successfully"
                else:
                    Logger.debug("No documents found with the given query")
                    return False, "No documents found with the given query"
            except Exception as e:
                Logger.error(
                    "Error occurred during delete_many operation", f"{e}"
                )
                return (
                    False,
                    "Error occurred during delete_many operation",
                )

    async def close_connection(self):
        try:
            self.client.close()
            Logger.info("Connection closed")
            return True, "Connection closed"
        except Exception as e:
            Logger.error("Error occurred during connection closing", f"{e}")
            return False, "Error occurred during connection closing"


async def example_usage():
    db_url = "mongodb://localhost:27017/"
    db_name = "test_database"
    collection_name = "test_collection"

    manager = MongoDBManager(db_url, db_name, collection_name)

    query = {"age": {"$gt": 25}}

    manager.read_manager.find_many(query)


# Running the asyncio event loop
if __name__ == "__main__":
    asyncio.run(example_usage())
