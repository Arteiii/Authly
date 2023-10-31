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
                    f"Document with ID {inserted_id} inserted successfully."
                )
                return True, inserted_id
            except Exception as e:
                Logger.debug(f"Error occurred while inserting document: {e}")
                return False, f"Error occurred while inserting document: {e}"

        async def insert_many_documents(self, data_list):
            try:
                await self.collection.insert_many(data_list)
                Logger.debug(f"Documents inserted successfully. ({data_list})")
                return True, "Documents inserted successfully."
            except Exception as e:
                Logger.debug(f"Error occurred while inserting documents: {e}")
                return False, f"Error occurred while inserting documents: {e}"

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
                    Logger.debug(f"Document found: {result}")
                    return True, result
                else:
                    Logger.debug("No document found with the given query.")
                    return False, result
            except Exception as e:
                Logger.debug(f"Error occurred during find_one operation: {e}")
                return False, f"Error occurred during find_one operation: {e}"

        async def find_many(self, query):
            try:
                result_list = []
                async for doc in self.collection.find(query):
                    result_list.append(doc)
                    Logger.debug(f"find many: {doc}")
                return True, result_list
            except Exception as e:
                Logger.debug(f"Error occurred during find_many operation: {e}")
                return False, f"Error occurred during find_many operation: {e}"

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
                    Logger.debug("Document updated successfully.")
                    return True, "Document updated successfully."
                else:
                    Logger.debug("No document found with the given query.")
                    return False, "No document found with the given query."
            except Exception as e:
                Logger.debug(
                    f"Error occurred during update_one operation: {e}"
                )
                return (
                    False,
                    f"Error occurred during update_one operation: {e}",
                )

        async def update_many_documents(self, query, update_data):
            try:
                result = await self.collection.update_many(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    print("Documents updated successfully.")
                    return True, "Documents updated successfully."
                else:
                    print("No document found with the given query.")
                    return False, "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during update_many operation: {e}")
                return (
                    False,
                    f"Error occurred during update_many operation: {e}",
                )

        async def replace_one_document(self, query, replace_data):
            try:
                result = await self.collection.replace_one(query, replace_data)
                if result.modified_count > 0:
                    print("Document replaced successfully.")
                    return True, "Document replaced successfully."
                else:
                    print("No document found with the given query.")
                    return False, "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during replace_one operation: {e}")
                return (
                    False,
                    f"Error occurred during replace_one operation: {e}",
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
                    print("Document deleted successfully.")
                    return True, "Document deleted successfully."
                else:
                    print("No document found with the given query.")
                    return False, "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during delete_document operation: {e}")
                return (
                    False,
                    f"Error occurred during delete_document operation: {e}",
                )

        async def delete_many_documents(self, query):
            try:
                result = await self.collection.delete_many(query)
                if result.deleted_count > 0:
                    print("Documents deleted successfully.")
                    return True, "Documents deleted successfully."
                else:
                    print("No documents found with the given query.")
                    return False, "No documents found with the given query."
            except Exception as e:
                print(f"Error occurred during delete_many operation: {e}")
                return (
                    False,
                    f"Error occurred during delete_many operation: {e}",
                )

    async def close_connection(self):
        try:
            self.client.close()
            return True, "Connection closed."
        except Exception as e:
            return False, f"Error occurred during connection closing: {e}"


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
