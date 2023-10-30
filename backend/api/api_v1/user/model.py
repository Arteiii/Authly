import base64
from typing import Dict, Optional

from core.config import config
from core.password_validation import validate_password_complexity
from core.username_validation import validate_username
from pydantic import BaseModel, EmailStr, Field, constr, validator


class UserDataResponse(BaseModel):
    user_data: Dict[str, Dict[str, str]]

    class Config:
        json_schema_extra = {
            "example": {
                "user_data": {
                    "abc#1234": {
                        "email": "user@example.com",
                        "username": "abc#1234",
                    }
                }
            }
        }


class UserRegistration(BaseModel):
    """
    Represents user registration data, including email, username, and password.
    """

    email: EmailStr = Field(..., example="1337@Allah.com")
    username: str = Field(..., example="abc#1234")
    password: constr(
        min_length=config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH,
        max_length=config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH,
    ) = Field(..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ==")
    # pw as base64 to prevent escaping characters in json

    @validator("password")
    def validate_password(cls, value):
        """
        Validate the password by decoding it as\
            Base64 and checking its complexity.

        Args:
            value (str): The password encoded as Base64.

        Returns:
            str: The decoded password if it passes validation.

        Raises:
            ValueError: If the decoding fails or the password\
                does not meet complexity requirements.
        """
        try:
            # Attempt to decode the password as Base64
            decoded_password = base64.b64decode(value.encode(), validate=True)
            decoded_password = decoded_password.decode()

            validate_password_complexity(decoded_password)

            # If the checks pass, return the decoded password
            return value

        except base64.binascii.Error as err:
            # If the decoding fails due to invalid Base64,
            # raise a validation error
            raise ValueError("Invalid Base64-encoded password") from err

    @validator("username")
    def validate_username(cls, value):
        # Define the regular expression pattern for the username
        validate_username(value)

        return value

    def json(self, *args, **kwargs):
        return dict(self)


class UserResult(BaseModel):
    mongo_results: str
    user_id: int
    username: str
    email: EmailStr


class GetUsersByName(BaseModel):
    usernames: list[str]


class GetLog(BaseModel):
    username: Optional[str]


class GetToken(BaseModel):
    username: str
    password: str
