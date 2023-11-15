import random
import string
from tokenize import TokenError
from authly.api.api_v1.db.connect import get_redis_manager
from authly.core.log import Logger, LogLevel
from authly.core.db.redis_crud import RedisManager


def generate_token(additional: int = 0) -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=64 + additional)
    )


def get_user_id(
    token: str, redis_manager: RedisManager = get_redis_manager()
) -> str:
    try:
        user_id = redis_manager.get(token)
        Logger.log(
            LogLevel.INFO,
            f"TOKEN: {token} tokentype({type(token)})",
            f"      \\__ UID: {user_id}",
        )
    except Exception as e:
        Logger.log(LogLevel.ERROR, "get user id exception:", e)
        raise TokenError("not found expired or invalid login")

    else:
        return user_id


def get_new_token(
    user_id: str,
    redis_manager: RedisManager = get_redis_manager(),
    expiration_time_minutes: int = 1440,
    token_length: int = 0,
) -> str:
    new_token = generate_token(token_length)
    try:
        redis_manager.connect()
        data = get_user_id(new_token, redis_manager)
        Logger.log(LogLevel.DEBUG, data)

    except TokenError as TE:
        Logger.log(LogLevel.DEBUG, "TokenError:", TE)

        set_result = redis_manager.set(
            new_token, user_id, expiration_seconds=expiration_time_minutes * 60
        )
        Logger.log(LogLevel.DEBUG, "set new token result:", set_result)

        Logger.log(
            LogLevel.DEBUG, "Redis manager close", redis_manager.close()
        )

        return new_token

    except Exception as e:
        raise Exception(f"exception while creating new token ({e})")

    else:
        Logger.log(
            LogLevel.DEBUG,
            f"found matching record for {new_token} in get_user_id("
            f"{data}) generating new one...",
        )
        get_new_token(user_id, redis_manager, token_length=+1)

        return ""
