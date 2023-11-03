import asyncio

from authly.core.db.redis import RedisManager
from authly.core.config import config
from authly.core.log import Logger

REDIS_HOST = config.RedisdbSettings.REDIS_HOST
REDIS_PORT = config.RedisdbSettings.REDIS_PORT
REDIS_DB = config.RedisdbSettings.REDIS_DB


# Create instances of the database managers
redis = RedisManager(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


# Test function to check the Redis operations
async def async_redis_operations() -> dict:
    test_results = {}

    # Connect to Redis
    connected = redis.connect()
    if connected:
        test_results["connection"] = "Passed"
    if not connected:
        Logger.critical("Failed to connect to Redis:", connected)
        return test_results

    # Perform a write operation
    key = "test_key"
    value = "test_value"
    write_result = redis.set(key, value)
    if write_result:
        test_results["write_operation"] = "Passed"
        Logger.debug("Value set successfully in Redis")
    else:
        test_results["write_operation"] = "Failed"
        Logger.error("Failed to set value in Redis")

    # Perform a read operation
    read_result = redis.get(key)
    if read_result:
        test_results["read_operation"] = "Passed"
        Logger.debug(f"Value retrieved from Redis: {read_result}")
    else:
        test_results["read_operation"] = "Failed"
        Logger.error("Failed to retrieve value from Redis")

    # Perform a delete operation
    delete_result = redis.delete(key)
    if delete_result:
        test_results["delete_operation"] = "Passed"
        Logger.debug("Key deleted successfully from Redis")
    else:
        test_results["delete_operation"] = "Failed"
        Logger.error("Failed to delete key from Redis")

    # Close the Redis connection
    closed = redis.close()
    if closed:
        test_results["close_connection"] = "Passed"
        Logger.debug("Redis connection closed successfully")
    else:
        test_results["close_connection"] = "Failed"
        Logger.error("Failed to close Redis connection")

    return {"Redis": [test_results]}


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_redis_operations())
