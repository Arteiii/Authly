from redis import asyncio as aioredis

from core.log import Logger


class AsyncRedisManager:
    def __init__(self, host, port, db):
        self.redis_client = None
        self.host = host
        self.port = port
        self.db = db

    async def connect(self):
        try:
            self.redis_client = await aioredis.create_redis_pool(
                f"redis://{self.host}:{self.port}/{self.db}"
            )
        except aioredis.RedisError as e:
            Logger.debug(f"Error connecting to Redis: {e}")
            return e
        return True

    async def close(self):
        try:
            self.redis_client.close()
            await self.redis_client.wait_closed()
        except aioredis.RedisError as e:
            Logger.debug(f"Error closing Redis connection: {e}")
            return e
        return True

    async def set(self, key, value, expiration=None):
        try:
            if expiration:
                await self.redis_client.setex(key, expiration, value)
            else:
                await self.redis_client.set(key, value)
        except aioredis.RedisError as e:
            Logger.debug(f"Error setting value in Redis: {e}")
            return e
        return True

    async def get(self, key):
        try:
            result = await self.redis_client.get(key)
            return result
        except aioredis.RedisError as e:
            Logger.debug(f"Error getting value from Redis: {e}")
            return e

    async def delete(self, key):
        try:
            await self.redis_client.delete(key)
        except aioredis.RedisError as e:
            Logger.debug(f"Error deleting key from Redis: {e}")
            return e
        return True
