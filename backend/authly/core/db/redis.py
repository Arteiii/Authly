import redis

from backend.authly.core.log import Logger


class RedisManager:
    def __init__(self, host, port, db):
        self.redis_client = None
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        try:
            self.redis_client = redis.Redis(
                host=self.host, port=self.port, decode_responses=True
            )
        except redis.RedisError as e:
            Logger.error(f"Error connecting to Redis: {e}")
            return False
        return True

    def close(self):
        try:
            self.redis_client.close()
        except redis.RedisError as e:
            Logger.error(f"Error closing Redis connection: {e}")
            return False
        return True

    def set(self, key, value, expiration=None):
        try:
            if expiration:
                self.redis_client.setex(key, expiration, value)
            else:
                self.redis_client.set(key, value)
        except redis.RedisError as e:
            Logger.error(f"Error setting value in Redis: {e}")
            return False
        return True

    def get(self, key):
        try:
            result = self.redis_client.get(key)
            return result
        except redis.RedisError as e:
            Logger.error(f"Error getting value from Redis: {e}")
            return False

    def delete(self, key):
        try:
            self.redis_client.delete(key)
        except redis.RedisError as e:
            Logger.error(f"Error deleting key from Redis: {e}")
            return False
        return True
