import random
import string
from core.db.redis import AsyncRedisManager
from core.config import config
from core.log import Logger


# import asyncio

# follow the instructions on how to install redis
# https://redis.io/docs/install/install-redis/

Redis_DB = config.RedisdbSettings.REDIS_DB
Redis_Port = config.RedisdbSettings.REDIS_PORT
Redis_Host = config.RedisdbSettings.REDIS_HOST


async def generate_access_token():
    # Generate a random string for the access token
    token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    return token


async def check_access_token_exists(redis_manager, user_id):
    # Check if the access token already exists in Redis
    existing_value = await redis_manager.get(user_id)
    if existing_value is not None:
        return existing_value  # Return the user object ID
    else:
        return None  # Access token does not exist


async def get_user_id(redis_manager, token):
    user_id = await redis_manager.get(token)
    if user_id is not None:
        return user_id
    else:
        return KeyError


async def create_token_for_uid(expiration_time_minutes=140):
    new_token = await generate_access_token()
    store_access_token(
        token=new_token,
        expiration_time=(expiration_time_minutes * 60),
    )


async def store_access_token(redis_manager, token, user_id, expiration_time):
    # Store the access token in Redis with the corresponding
    # user object ID and an expiration time

    results = await redis_manager.set(token, user_id, expiration_time)

    return results


async def main(
    user_id,
    token,
    db=Redis_DB,
    port=Redis_Port,
    host=Redis_Host,
    expiration_time_minutes=140,
):
    redis_manager = AsyncRedisManager(db=db, port=port, host=host)
    await redis_manager.connect()

    if token:
        uid = get_user_id(redis_manager, token)
        Logger.info(f"TOKEN: {token}\n \\__ UID: {uid}")
        return uid

    existing_token = await check_access_token_exists(redis_manager, user_id)

    if existing_token:
        await redis_manager.delete(existing_token)

    new_token = await generate_access_token()
    await store_access_token(
        redis_manager, new_token, user_id, expiration_time_minutes
    )

    # Close the Redis connection
    await redis_manager.close()

    return new_token
