"""
MongoDBClient Module

This module provides an asyncio-compatible\
MongoDB client for performing database operations
such as insertion, retrieval, and updates.
It is designed to work with a MongoDB database\
specified by the connection URL and database name.

Author: Arteii
Date: 24/10/2023
"""

import motor.motor_asyncio
from core.config import config
from pymongo.errors import DuplicateKeyError


class MongoDBClient:
    def __init__(
        self,
        mongodb_url=config.MongodbSettings.MONGODB_URL,
        db_name=config.MongodbSettings.MONGODB_NAME,
    ):
        """
        Initialize the MongoDB client.

        Args:
            mongodb_url (str): The MongoDB connection URL.
            db_name (str): The name of the database to use.

        Initializes the MongoDB client and connects to the specified database.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        self.db = self.client[db_name]

    async def insert_document(self, collection_name, document):
        """
        Insert a document into a MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to insert.

        Returns:
            str: The inserted document's _id.

        Inserts a document into the specified collection and\
            returns the _id of the inserted document.
        If a duplicate key error occurs, it returns None.
        """
        try:
            result = await self.db[collection_name].insert_one(document)
            return result.inserted_id
        except DuplicateKeyError:
            return None  # Handle duplicate key error as needed

    async def find_document_by_dict(self, collection_name, search: dict):
        """
        Find documents in a MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            filter (dict): The filter criteria.

        Returns:
            list: List of documents that match the filter.

        Finds documents in the specified collection based on the filter\
            criteria and returns a list of matching documents.
        """
        document = await self.db[collection_name].find_one(search)

        if document:
            return document

        return {"message": f"{search}not found"}

    async def find_document_by_id(self, collection_name, document_id):
        """
        Find a document in a MongoDB collection by _id.

        Args:
            collection_name (str): The name of the collection.
            document_id (str): The _id of the document to find.

        Returns:
            dict: The found document or None if not found.

        Finds a document in the specified collection by its _id and\
            returns the document.
        If not found, it returns None.
        """
        document = await self.db[collection_name].find_one({"_id": document_id})
        return document

    async def update_document(self, collection_name, document_id, update_data):
        """
        Update a document in a MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            document_id (str): The _id of the document to update.
            update_data (dict): The data to update.

        Returns:
            int: The number of documents modified.

        Updates a document in the specified collection by its _id with\
            the provided update data.
        Returns the number of documents modified.
        """
        result = await self.db[collection_name].update_one(
            {"_id": document_id}, {"$set": update_data}
        )
        return result.modified_count

    async def delete_document(self, collection_name, document_id):
        """
        Delete a document from a MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            document_id (str): The _id of the document to delete.

        Returns:
            int: The number of documents deleted.

        Deletes a document from the specified collection by its _id.
        Returns the number of documents deleted.
        """
        result = await self.db[collection_name].delete_one({"_id": document_id})
        return result.deleted_count

    async def close(self):
        """
        Close the MongoDB client.

        Closes the MongoDB client and its connections.
        """
        self.client.close()
