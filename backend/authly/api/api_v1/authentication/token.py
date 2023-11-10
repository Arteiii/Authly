import random
import string
from authly.core.db.redis_crud import RedisManager
from authly.core.config import application_config
from authly.core.log import Logger
from authly.core.log import LogLevel

Redis_DB = application_config.RedisdbSettings.REDIS_DB
Redis_Port = application_config.RedisdbSettings.REDIS_PORT
Redis_Host = application_config.RedisdbSettings.REDIS_HOST


def generate_token():
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))


def check_access_token_exists(redis_manager, user_id):
    existing_value = redis_manager.get(user_id)
    return existing_value


def get_user_id(redis_manager, token):
    user_id = redis_manager.get(token)
    Logger.log(LogLevel.DEBUG, user_id)
    return user_id


def create_token_for_uid(redis_manager, user_id, expiration_time_minutes=140):
    new_token = generate_token()
    store_access_token(
        redis_manager, new_token, user_id, expiration_time_minutes
    )
    return new_token


def store_access_token(redis_manager, token, user_id, expiration_time):
    results = redis_manager.set(token, user_id, expiration_time)
    return results


def Token(
    user_id: str = None,
    token: str = None,
    db: str = Redis_DB,
    port: int = Redis_Port,
    host: str = Redis_Host,
    expiration_time_minutes: int = 999999,
) -> tuple[bool, dict]:
    redis_manager = RedisManager(redis_host=host, redis_port=port, redis_db=db)
    redis_manager.connect()

    if token:
        uid = get_user_id(redis_manager, token)
        if uid != "None":
            Logger.log(LogLevel.INFO, f"TOKEN: {token}", f"\\__ UID: {uid}")
            return True, uid
        return False, "invalid uid"

    existing_token = check_access_token_exists(redis_manager, user_id)

    if existing_token:
        redis_manager.delete(existing_token)

    new_token = create_token_for_uid(
        redis_manager, user_id, expiration_time_minutes
    )

    redis_manager.close()

    return True, new_token
