"""
main.py
"""

from authly.core.db.mongo_crud import MongoDBManager
from authly.core.db.redis_crud import RedisManager

from authly.core.config import application_config


class MongoConfig:
    mongo_config = application_config.MongodbSettings  # type: ignore
    name = mongo_config.MONGODB_NAME
    url = mongo_config.MONGODB_URL


class RedisConfig:
    redis_config = application_config.RedisdbSettings  # type: ignore
    db = redis_config.REDIS_DB
    host = redis_config.REDIS_HOST
    port = redis_config.REDIS_PORT


def get_mongo_manager(
    collection_name: str,
    db_url: str = MongoConfig.url,
    db_name: str = MongoConfig.name,
) -> MongoDBManager:
    return MongoDBManager(db_url, db_name, collection_name)


def get_redis_manager(
    redis_port: int = RedisConfig.port,
    redis_db: int = RedisConfig.db,
    redis_host: str = RedisConfig.host,
) -> RedisManager:
    return RedisManager(redis_port, redis_db, redis_host)
