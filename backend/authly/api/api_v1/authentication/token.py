import random
import string
from backend.authly.core.db.redis import RedisManager
from backend.authly.core.config import config
from backend.authly.core.log import Logger

# follow the instructions on how to install redis
# https://redis.io/docs/install/install-redis/

Redis_DB = config.RedisdbSettings.REDIS_DB
Redis_Port = config.RedisdbSettings.REDIS_PORT
Redis_Host = config.RedisdbSettings.REDIS_HOST


def generate_token():
    # Generate a random string for the access token
    token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    return token


def check_access_token_exists(redis_manager, user_id):
    # Check if the access token already exists in Redis
    existing_value = redis_manager.get(user_id)
    if existing_value is not None:
        return existing_value  # Return the user object ID
    else:
        return None  # Access token does not exist


def get_user_id(redis_manager, token):
    user_id = redis_manager.get(token)
    Logger.debug(user_id)
    if user_id is not None:
        return user_id
    else:
        return KeyError


async def create_token_for_uid(expiration_time_minutes=140):
    new_token = generate_token()
    store_access_token(
        token=new_token,
        expiration_time=(expiration_time_minutes * 60),
    )


def store_access_token(redis_manager, token, user_id, expiration_time):
    # Store the access token in Redis with the corresponding
    # user object ID and an expiration time

    results = redis_manager.set(token, user_id, expiration_time)

    return results


def Token(
    user_id: str = None,
    token: str = None,
    db: str = Redis_DB,
    port: int = Redis_Port,
    host: str = Redis_Host,
    expiration_time_minutes: int = 140,
):
    redis_manager = RedisManager(db=db, port=port, host=host)
    redis_manager.connect()

    if token:
        uid = get_user_id(redis_manager, token)
        Logger.info(f"TOKEN: {token}\n", f"\\__ UID: {uid}")

        return uid

    existing_token = check_access_token_exists(redis_manager, user_id)

    if existing_token:
        redis_manager.delete(existing_token)

    new_token = generate_token()
    store_access_token(
        redis_manager=redis_manager,
        token=new_token,
        user_id=user_id,
        expiration_time=expiration_time_minutes,
    )

    # Close the Redis connection
    redis_manager.close()

    return new_token
