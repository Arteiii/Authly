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
                await self.collection.insert_one(data)
                print("Document inserted successfully.")
                return "Document inserted successfully."
            except Exception as e:
                print(f"Error occurred while inserting document: {e}")
                return f"Error occurred while inserting document: {e}"

        async def insert_many_documents(self, data_list):
            try:
                await self.collection.insert_many(data_list)
                print(f"Documents inserted successfully. ({data_list})")
                return "Documents inserted successfully."
            except Exception as e:
                print(f"Error occurred while inserting documents: {e}")
                return f"Error occurred while inserting documents: {e}"

        async def bulk_write(self, requests):
            try:
                result = await self.collection.bulk_write(requests)
                print(f"{result.inserted_count} documents inserted.")
                print(f"{result.modified_count} documents updated.")
                print(f"{result.deleted_count} documents deleted.")
                return (
                    result.inserted_count,
                    result.modified_count,
                    result.deleted_count,
                )
            except Exception as e:
                print(f"Error occurred during bulk write operation: {e}")
                return f"Error occurred during bulk write operation: {e}"

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
                    print("Document found:", result)
                    return result
                else:
                    print("No document found with the given query.")
                    return "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during find_one operation: {e}")
                return f"Error occurred during find_one operation: {e}"

        async def find_many(self, query):
            try:
                result_list = []
                async for doc in self.collection.find(query):
                    result_list.append(doc)
                    print(doc)
                return result_list
            except Exception as e:
                print(f"Error occurred during find_many operation: {e}")
                return f"Error occurred during find_many operation: {e}"

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
                    print("Document updated successfully.")
                    return "Document updated successfully."
                else:
                    print("No document found with the given query.")
                    return "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during update_one operation: {e}")
                return f"Error occurred during update_one operation: {e}"

        async def update_many_documents(self, query, update_data):
            try:
                result = await self.collection.update_many(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    print("Documents updated successfully.")
                    return "Documents updated successfully."
                else:
                    print("No document found with the given query.")
                    return "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during update_many operation: {e}")
                return f"Error occurred during update_many operation: {e}"

        async def replace_one_document(self, query, replace_data):
            try:
                result = await self.collection.replace_one(query, replace_data)
                if result.modified_count > 0:
                    print("Document replaced successfully.")
                    return "Document replaced successfully."
                else:
                    print("No document found with the given query.")
                    return "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during replace_one operation: {e}")
                return f"Error occurred during replace_one operation: {e}"

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
                    return "Document deleted successfully."
                else:
                    print("No document found with the given query.")
                    return "No document found with the given query."
            except Exception as e:
                print(f"Error occurred during delete_document operation: {e}")
                return f"Error occurred during delete_document operation: {e}"

        async def delete_many_documents(self, query):
            try:
                result = await self.collection.delete_many(query)
                if result.deleted_count > 0:
                    print("Documents deleted successfully.")
                    return "Documents deleted successfully."
                else:
                    print("No documents found with the given query.")
                    return "No documents found with the given query."
            except Exception as e:
                print(f"Error occurred during delete_many operation: {e}")
                return f"Error occurred during delete_many operation: {e}"

    async def close_connection(self):
        try:
            self.client.close()
            return "Connection closed."
        except Exception as e:
            return f"Error occurred during connection closing: {e}"


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
