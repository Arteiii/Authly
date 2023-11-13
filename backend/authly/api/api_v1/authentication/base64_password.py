import base64
import binascii

from backend.authly.core.log import Logger, LogLevel
from backend.authly.core.password_validation import (
    validate_password_complexity,
)


def encode_to_base64(value: str) -> str:
    try:
        encoded_password = base64.b64encode(value.encode()).decode()
        return encoded_password
    except Exception as e:
        Logger.log(LogLevel.ERROR, f"Invalid Base64-encoded password ({e})")
        raise ValueError(
            "Error occurred while encoding to Base64: (more in logs)"
        )


def decode_base64(value: str) -> str:
    try:
        decoded_password = base64.b64decode(
            value.encode(), validate=True
        ).decode()
        return decoded_password
    except binascii.Error as err:
        Logger.log(LogLevel.ERROR, f"Invalid Base64-encoded password ({err})")
        raise ValueError("Invalid Base64-encoded password: (more in logs)")


def validate_base64_password(value: str) -> str:
    decoded_password = decode_base64(value)
    validate_password_complexity(
        decoded_password
    )  # Assuming you have this function defined
    return value
