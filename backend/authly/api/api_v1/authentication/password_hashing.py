from authly.core.hashing import Hasher
from authly.core.log import Logger, LogLevel
from authly.core.config import application_config
import time

password_config = application_config.PasswordConfig  # type: ignore


async def hash_password(password) -> str:
    start_time = time.time()  # Record the start time

    hashed = Hasher.get_password_hash(password=password)

    end_time = time.time()  # Record the end time

    Logger.log(
        LogLevel.DEBUG,
        f"using: {password_config.HASHING_ALGORITHM}",
        f"Hashed Password: {hashed}",
        f"Hashing Time: {end_time - start_time} seconds",
    )

    return hashed


async def verify_password(password, stored_hash):
    start_time = time.time()  # Record the start time

    result = Hasher.verify_password(password, stored_hash)
    end_time = time.time()

    Logger.log(
        LogLevel.DEBUG,
        f"using: {password_config.HASHING_ALGORITHM}",
        f"verify password result:: {result}",
        f"Hashing Time: {end_time - start_time} seconds",
    )

    return result
