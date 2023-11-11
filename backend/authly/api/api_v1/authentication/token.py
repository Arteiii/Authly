import random
import string
from authly.core.log import Logger, LogLevel
from authly.core.db.redis_crud import RedisManager


def generate_token(additional: int = 0):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=64 + additional)
    )


def get_user_id(
    token: str, redis_manager: RedisManager
) -> tuple[bool, str | None, str]:
    Logger.log(LogLevel.DEBUG, token, type(token))
    (status, user_id, details) = redis_manager.get(str(token))
    if status is False:
        Logger.log(
            LogLevel.INFO,
            f"TOKEN: {token}",
            f"      \\__ UID: {user_id}",
            f"status({status})",
            f"user_id({user_id})",
            f"details({details})",
        )
        return (True, user_id, f"valid token({token}), uid({user_id})")
    return (False, None, "invalid uid")


def get_new_token(
    user_id: str,
    redis_manager: RedisManager,
    expiration_time_minutes: int = 1440,
    token_length: int = 0,
) -> tuple[bool, str, str]:
    new_token = generate_token(token_length)
    (status, data, details) = get_user_id(new_token, redis_manager)
    Logger.log(LogLevel.DEBUG, status, data, details)
    if status is True:
        Logger.log(
            LogLevel.DEBUG,
            f"found matching record for {new_token} in get_user_id("
            f"{get_user_id(new_token, redis_manager)}) generating new one...",
        )
        get_new_token(user_id, redis_manager, token_length=+1)

    (status, data, details) = redis_manager.set(
        new_token, user_id, expiration_seconds=expiration_time_minutes * 60
    )
    Logger.log(
        LogLevel.DEBUG,
        f"status({status})",
        f"data({data})",
        f"details({details})",
    )
    return (True, new_token, details)
