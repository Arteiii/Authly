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
            """
            Initialize the WriteManager class.

            Args:
                collection: The MongoDB collection to manage.
            """
            self.collection = collection

        async def insert_document(self, data) -> tuple[bool, str | None, str]:
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
            try:
                result = await self.collection.insert_one(data)
                inserted_id = str(result.inserted_id)
                return (
                    True,
                    inserted_id,
                    f"Document with ID {inserted_id} inserted successfully",
                )
            except Exception as e:
                return (
                    False,
                    None,
                    "Error occurred while inserting document" f"{e}",
                )

        async def insert_many_documents(
            self, data_list
        ) -> tuple[bool, str, str]:
            """
            Insert multiple documents into the MongoDB collection.

            Args:
                data_list: A list of documents to insert.

            Returns:
                A tuple containing:
                - bool: True if the insertion was successful, False otherwise.
                - str: A descriptive message about the insertion result.
                - str: Additional information about the inserted documents.
            """
            try:
                await self.collection.insert_many(data_list)
                return (
                    True,
                    "Documents inserted successfully",
                    "Documents inserted successfully:" f"{data_list}",
                )
            except Exception as e:
                return (
                    False,
                    "Error occurred while inserting documents",
                    "Error occurred while inserting documents:" f"{e}",
                )

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

        async def find_one(self, query) -> tuple[bool, dict, str]:
            """
            Find one document in the MongoDB collection based on\
                the given query.

            Args:
                query: The query to find the document.

            Returns:
                A tuple containing:
                - bool: True if a document was found, False otherwise.
                - str or None: The found document if successful,\
                    None otherwise.
                - str: A descriptive message about the find_one result.
            """
            try:
                result = await self.collection.find_one(query)
                if result:
                    return True, result, "Document found" f"{result}"
                else:
                    return (
                        False,
                        result,
                        "No document found with the given query:" f"{query}",
                    )
            except Exception as e:
                return (
                    False,
                    result,  # type: ignore
                    "Error occurred during find_one operation" f"{e}",
                )

        async def find_many(self, query) -> tuple[bool, list | None, str]:
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
            try:
                result_list = []
                async for doc in self.collection.find(query):
                    result_list.append(doc)
                return (True, result_list, "find many" f"{query}")
            except Exception as e:
                return (
                    False,
                    None,
                    "Error occurred during find_many operation" f"{e}",
                )

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
            self, query, update_data
        ) -> tuple[bool, str, str]:
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
            try:
                result = await self.collection.update_one(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    return (
                        True,
                        "Document updated successfully",
                        "Document updated successfully: "
                        f"query({query}), updatedata ({update_data})",
                    )
                else:
                    return (
                        False,
                        "No document found with the given query",
                        "No document found with the given query"
                        f"query({query}), updatedata ({update_data})",
                    )
            except Exception as e:
                return (
                    False,
                    "Error occurred during update_one operation",
                    "Error occurred during update_one operation" f"{e}",
                )

        async def update_many_documents(
            self, query, update_data
        ) -> tuple[bool, str, str]:
            """
            Update multiple documents in the MongoDB collection based on the\
                given query.

            Args:
                query: The query to find the documents.
                update_data: The data to update in the documents.

            Returns:
                A tuple containing:
                - bool: True if the update was successful, False otherwise.
                - str: A descriptive message about the update result.
                - str: Additional information about the update operation.
            """
            try:
                result = await self.collection.update_many(
                    query, {"$set": update_data}
                )
                if result.modified_count > 0:
                    return (
                        True,
                        "Documents updated successfully",
                        "Documents updated successfully"
                        f"query({query}), update_data({update_data})",
                    )
                else:
                    return (
                        False,
                        "No document found with the given query",
                        "No document found with the given query"
                        f"query({query}), update_data({update_data})",
                    )
            except Exception as e:
                return (
                    False,
                    "Error occurred during update_many operation",
                    "Error occurred during update_many operation" f"{e}",
                )

        async def replace_one_document(
            self, query, replace_data
        ) -> tuple[bool, str, str]:
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
            try:
                result = await self.collection.replace_one(query, replace_data)
                if result.modified_count > 0:
                    return (
                        True,
                        "Document replaced successfully",
                        "Document replaced successfully"
                        f" query({query}), replace_data({replace_data})",
                    )
                else:
                    return (
                        False,
                        "No document found with the given query",
                        "No document found with the given query"
                        f" query({query}), replace_data({replace_data})",
                    )
            except Exception as e:
                return (
                    False,
                    "Error occurred during replace_one operation",
                    "Error occurred during replace_one operation" f"{e}",
                )

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

        async def delete_document(self, query) -> tuple[bool, str, str]:
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
            try:
                result = await self.collection.delete_one(query)
                if result.deleted_count > 0:
                    return (
                        True,
                        "Document deleted successfully",
                        "Document deleted successfully" f"query({query})",
                    )
                else:
                    return (
                        False,
                        "No document found with the given query",
                        "No document found with the given query"
                        f"query({query})",
                    )
            except Exception as e:
                return (
                    False,
                    "Error occurred during delete_document operation",
                    "Error occurred during delete_document operation" f"{e}",
                )

        async def delete_many_documents(self, query) -> tuple[bool, str, str]:
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
            try:
                result = await self.collection.delete_many(query)
                if result.deleted_count > 0:
                    return (
                        True,
                        "Documents deleted successfully",
                        "Documents deleted successfully" f"query({query})",
                    )
                else:
                    return (
                        False,
                        "No documents found with the given query",
                        "No documents found with the given query"
                        f"query({query})",
                    )
            except Exception as e:
                return (
                    False,
                    "Error occurred during delete_many operation",
                    "Error occurred during delete_many operation" f"{e}",
                )

    async def close_connection(self) -> tuple[bool, str, str]:
        """
        Close the MongoDB connection.

        Returns:
            A tuple containing:
            - bool: True if the connection was closed successfully,\
                False otherwise.
            - str: A descriptive message about the connection closure result.
            - str: Additional information or error message if applicable.
        """
        try:
            self.client.close()
            return True, "Connection closed", "Connection closed"
        except Exception as e:
            return (
                False,
                "Error occurred during connection closing",
                "Error occurred during connection closing" f"{e}",
            )


async def example_usage():
    db_url = "mongodb://localhost:27017/"
    db_name = "test_database"
    collection_name = "test_collection"

    manager = MongoDBManager(db_url, db_name, collection_name)

    query = {"age": {"$gt": 25}}

    manager.read_manager.find_many(query)  # type: ignore


# Running the asyncio event loop
if __name__ == "__main__":
    asyncio.run(example_usage())
