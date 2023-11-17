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

Author: Arteii
Date: 25/10/2023
"""

from typing import Any, Tuple
import motor.motor_asyncio


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
        self.client: motor.motor_asyncio.AsyncIOMotorClient = (
            motor.motor_asyncio.AsyncIOMotorClient(db_url)
        )
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client[
            db_name
        ]
        self.collection: motor.motor_asyncio.AsyncIOMotorCollection = self.db[
            collection_name
        ]
        self.update_manager = self.UpdateManager(self.collection)
        self.write_manager = self.WriteManager(self.collection)
        self.delete_manager = self.DeleteManager(self.collection)
        self.read_manager = self.ReadManager(self.collection)

    #####################################
    #               Write:             #
    #####################################

    class WriteManager:
        def __init__(self, collection):
            """
            Initialize the WriteManager class.

            Args:
                collection: The MongoDB collection to manage.
            """
            self.collection = collection

        async def insert_document(self, data: dict) -> Tuple[bool, Any]:
            """
            Insert a document into the MongoDB collection.

            Args:
                data: The document data to insert.

            Returns:
                A tuple containing:
                - bool: True if the insertion was successful, False otherwise.
                - str or None: The inserted document's ID if successful,\
                    None otherwise.
                - str: A descriptive message about the insertion result.
            """

            result = await self.collection.insert_one(data)

            if result:
                return (
                    True,
                    result.inserted_id,
                )

            return False, result

    #####################################
    #                Read:              #
    #####################################

    class ReadManager:
        def __init__(self, collection):
            """
            Initialize the ReadManager class.

            Args:
                collection: The MongoDB collection to manage.
            """
            self.collection = collection

        async def find_one(self, query: dict) -> Tuple[bool, dict]:
            """
            Find one document in the MongoDB collection based on\
                the given query.

            Args:
                query: The query to find the document.

            Returns:
                A tuple containing:
                - bool: True if a document was found, False otherwise.
                - str with the reults

            Raise:
                - Exception(f"An unexpected error occurred: {e}")
                - FileNotFoundError("Mongo search Result is False")
            """
            result = await self.collection.find_one(query)

            if result:
                return True, result

            return False, result

        async def find_many(self, query: dict) -> Tuple[bool, list]:
            """
            Find multiple documents in the MongoDB collection\
                based on the given query.

            Args:
                query: The query to find the documents.

            Returns:
                A tuple containing:
                - bool: True if documents were found, False otherwise.
                - list or None: The list of found documents if successful,\
                    None otherwise.
                - str: A descriptive message about the find_many result.
            """
            result_list: list = []
            async for doc in self.collection.find(query):
                result_list.append(doc)

            if result_list:
                return True, result_list

            return False, result_list

    #####################################
    #               Update:             #
    #####################################

    class UpdateManager:
        def __init__(self, collection):
            """
            Initialize the UpdateManager class.

            Args:
                collection: The MongoDB collection to manage.
            """
            self.collection = collection

        async def update_one_document(
            self, query: dict, update_data: dict
        ) -> Tuple[bool, Any]:
            """
            Update a single document in the MongoDB collection based on the\
                given query.

            Args:
                query: The query to find the document.
                update_data: The data to update in the document.

            Returns:
                A tuple containing:
                - bool: True if the update was successful, False otherwise.
                - str: A descriptive message about the update result.
                - str: Additional information about the update operation.
            """
            result = await self.collection.update_one(
                query, {"$set": update_data}
            )

            if result.modified_count > 0:
                return True, result

            return False, result

        async def replace_one_document(
            self, query: dict, replace_data: dict
        ) -> Tuple[bool, Any]:
            """
            Replace a single document in the MongoDB collection based on the\
                given query.

            Args:
                query: The query to find the document.
                replace_data: The data to replace in the document.

            Returns:
                A tuple containing:
                - bool: True if the replacement was successful,\
                    False otherwise.
                - str: A descriptive message about the replacement result.
                - str: Additional information about the replacement operation.
            """
            result = await self.collection.replace_one(query, replace_data)

            if result.modified_count > 0:
                return (True, result)

            return (False, result)

    #####################################
    #               Delete:             #
    #####################################
    class DeleteManager:
        def __init__(self, collection):
            """
            Initialize the DeleteManager class.

            Args:
                collection: The MongoDB collection to manage.
            """
            self.collection = collection

        async def delete_document(self, query: dict) -> Tuple[bool, Any]:
            """
            Delete a single document from the MongoDB collection based on the\
                given query.

            Args:
                query: The query to find the document.

            Returns:
                A tuple containing:
                - bool: True if the deletion was successful, False otherwise.
                - str: A descriptive message about the deletion result.
                - str: Additional information about the deletion operation.
            """
            result = await self.collection.delete_one(query)

            if result.deleted_count > 0:
                return True, result

            return (False, result)

        async def delete_many_documents(self, query: dict) -> Tuple[bool, Any]:
            """
            Delete multiple documents from the MongoDB collection based on the\
                given query.

            Args:
                query: The query to find the documents.

            Returns:
                A tuple containing:
                - bool: True if the deletions were successful, False otherwise.
                - str: A descriptive message about the deletion result.
                - str: Additional information about the deletion operation.
            """

            result = await self.collection.delete_many(query)

            if result.deleted_count > 0:
                return True, result

            return (False, result)

    async def close_connection(self) -> Tuple[bool, Any]:
        """
        Close the MongoDB connection.

        Returns:
            A tuple containing:
            - bool: True if the connection was closed successfully,\
                False otherwise.
            - str: A descriptive message about the connection closure result.
            - str: Additional information or error message if applicable.
        """
        self.client.close()
        return True, "Connection closed"
