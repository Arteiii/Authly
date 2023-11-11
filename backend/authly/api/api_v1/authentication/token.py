import random
import string
from authly.core.log import Logger, LogLevel


def generate_token():
    return "".join(random.choices(string.ascii_letters + string.digits, k=128))


def get_user_id(token: str, redis_manager) -> tuple[bool, str | None, str]:
    user_id = redis_manager.get(token)
    if user_id != "None":
        Logger.log(
            LogLevel.INFO, f"TOKEN: {token}", f"         \\__ UID: {user_id}"
        )
        return (True, user_id, f"valid token({token}), uid({user_id})")
    return (False, None, "invalid uid")


def get_new_token(
    user_id: str, redis_manager, expiration_time_minutes: int = 1440
) -> tuple[bool, str, str]:
    new_token = generate_token()
    if get_user_id(new_token, redis_manager) is None:
        Logger.log(
            LogLevel.DEBUG,
            f"found matching record for {new_token} in get_user_id("
            f"{get_user_id(new_token, redis_manager)}) generating new one...",
        )
        get_new_token(user_id, redis_manager)

    result = redis_manager.set(
        new_token, user_id, expiration_time_minutes * 60
    )
    return (
        True,
        new_token,
        f"new token({new_token}) for uid({user_id}) with result({result})",
    )
