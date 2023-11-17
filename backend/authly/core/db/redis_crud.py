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
        self.redis_client: redis.Redis
        self.host = redis_host
        self.port = redis_port
        self.db = redis_db

    def connect(self) -> bool:
        """
        Connect to the Redis server.

        Returns:
            - bool: True if the connection was closed successfully.

        Raises:
            - AuthenticationError
            - RedisError: If there is an error during the set operation.
        """
        self.redis_client: redis.Redis = redis.Redis(
            host=self.host, port=self.port, decode_responses=True
        )
        return True

    def close(self) -> bool:
        """
        Close the connection to the Redis server.

        Returns:
            - bool: True if the connection was closed successfully.

        Raises:
            RedisError: If there is an error during the set operation.
        """
        self.redis_client.close()
        return True

    def set(self, key: str, value: str, expiration_seconds: int = 0) -> bool:
        """
        Set a key-value pair in Redis.

        Args:
            key (str): The key to set.
            value (str): The value to set.
            expiration (int): The expiration time for the key-value pair in\
                seconds (default is 0).

        Returns:
            - bool: True if the set operation was successful.

        Raises:
            RedisError: If there is an error during the set operation.
        """
        if expiration_seconds:
            self.redis_client.setex(key, expiration_seconds, value)
        else:
            self.redis_client.set(key, value)

        return True

    def get(self, key: str) -> str:
        """
        Get the value associated with a key in Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            - str of the results

        Raises:
            RedisError: If there is an error during the set operation.
        """
        result = self.redis_client.get(key)

        return str(result)

    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.

        Args:
            key (str): The key to delete.

        Returns:
            - bool: True if the delete operation was successful.

        Raises:
            RedisError: If there is an error during the set operation.
        """
        self.redis_client.delete(key)

        return True

    def exists(self, key: str) -> int:
        result = self.redis_client.exists(key)

        return result  # type: ignore
