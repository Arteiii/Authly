"""
Redis Manager Module

This module defines a RedisManager class for interacting with a Redis server. \
It provides methods to connect to the server, \
    set and retrieve key-value pairs, and close the connection.

Usage:
    from redis_manager import RedisManager

    # Create an instance of RedisManager
    redis_manager = RedisManager(redis_port=6379, redis_db=0,\
        redis_host='localhost')

    # Connect to the Redis server
    success, _, message = redis_manager.connect()

    # Set a key-value pair in Redis
    success, _, message = redis_manager.set(key='example_key',\
        value='example_value')

    # Retrieve the value associated with a key
    success, result, message = redis_manager.get(key='example_key')
    if success:
        print(f"Value for 'example_key': {result}")

    # Close the connection to the Redis server
    success, _, message = redis_manager.close()

Author: Arteii
Date: 25/10/2023
"""


import redis


class RedisManager:
    def __init__(
        self, redis_port: int, redis_db: int, redis_host: str = "localhost"
    ):
        """
        Initialize the RedisManager class.

        Args:
            redis_port (int): The port of the Redis server.
            redis_db (int): The Redis database number.
            redis_host (str): The host address of the Redis server\
                (default is "localhost").
        """
        self.redis_client = None
        self.host = redis_host
        self.port = redis_port
        self.db = redis_db

    def connect(self) -> tuple[bool, str, str]:
        """
        Connect to the Redis server.

        Returns:
            A tuple containing:
            - bool: True if the connection was successful, False otherwise.
            - str: None.
            - str: A descriptive message about the connection result.
        """
        try:
            self.redis_client = redis.Redis(
                host=self.host, port=self.port, decode_responses=True
            )
        except redis.RedisError as e:
            return (False, None, f"Error connecting to Redis: {e}")
        return (True, None, "Succesfully!")

    def close(self) -> tuple[bool, str, str]:
        """
        Close the connection to the Redis server.

        Returns:
            A tuple containing:
            - bool: True if the connection was closed successfully,\
                False otherwise.
            - str: None.
            - str: A descriptive message about the closure result.
        """
        try:
            self.redis_client.close()
        except redis.RedisError as e:
            return (False, None, f"Error closing Redis connection: {e}")
        return (True, None, "Succesfully!")

    def set(
        self, key: any, value: any, expiration_seconds: int = None
    ) -> tuple[bool, str, str]:
        """
        Set a key-value pair in Redis.

        Args:
            key (any): The key to set.
            value (any): The value to set.
            expiration (int): The expiration time for the key-value pair in\
                seconds (default is None).

        Returns:
            A tuple containing:
            - bool: True if the set operation was successful, False otherwise.
            - str: None.
            - str: A descriptive message about the set operation.
        """
        try:
            if expiration_seconds:
                self.redis_client.setex(key, expiration_seconds, value)
            else:
                self.redis_client.set(key, value)
        except redis.RedisError as e:
            return (False, None, f"Error setting value in Redis: {e}")
        return (
            True,
            None,
            "Succesfully inserted:"
            f"key({key}), value({value}), expiration({expiration_seconds})",
        )

    def get(self, key: any) -> tuple[bool, str, str]:
        """
        Get the value associated with a key in Redis.

        Args:
            key (any): The key to retrieve.

        Returns:
            A tuple containing:
            - bool: True if the get operation was successful, False otherwise.
            - str: The retrieved value if successful, None otherwise.
            - str: A descriptive message about the get operation.
        """
        try:
            result = self.redis_client.get(key)
            return (True, result, f"get key({key})")
        except redis.RedisError as e:
            return (False, None, f"Error getting value from Redis: {e}")

    def delete(self, key: any) -> tuple[bool, str, str]:
        """
        Delete a key from Redis.

        Args:
            key (any): The key to delete.

        Returns:
            A tuple containing:
            - bool: True if the delete operation was successful,\
                False otherwise.
            - str: None.
            - str: A descriptive message about the delete operation.
        """
        try:
            self.redis_client.delete(key)
        except redis.RedisError as e:
            return (False, None, f"Error deleting key from Redis: {e}")
        return (True, None, f"Deleted: key({key})")
