import base64
from typing import Dict, List, Optional
from backend.authly.core.log import Logger

from backend.authly.core.config import application_config
from backend.authly.core.password_validation import (
    validate_password_complexity,
)
from pydantic import BaseModel, EmailStr, Field, constr, validator


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
    except base64.binascii.Error as err:
        Logger.log(LogLevel.ERROR, f"Invalid Base64-encoded password ({err})")
        raise ValueError("Invalid Base64-encoded password: (more in logs)")


def validate_base64_password(value: str) -> str:
    decoded_password = decode_base64(value)
    validate_password_complexity(
        decoded_password
    )  # Assuming you have this function defined
    return value


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
    email: EmailStr = Field(..., example="1337@Allah.com")
    username: str = Field(..., example="abc#1234")
    password: constr(
        min_length=application_config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH,
        max_length=application_config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH,
    ) = Field(..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ==")

    @validator("password")
    def validate_password(cls, value):
        return validate_base64_password(value)

    def json(self, *args, **kwargs):
        self.password = encode_to_base64(self.password)
        return dict(self)


class LoginRequest(BaseModel):
    email: Optional[EmailStr]
    user_id: Optional[str]
    password: str

    @validator("password")
    def validate_password(cls, value):
        return validate_base64_password(value)


class DeleteUser(BaseModel):
    user_id: List[str]


class DeleteUserResponse(BaseModel):
    overall_status: bool
    details: List[Dict[str, bool]]


class UpdateUsername(BaseModel):
    user_id: str
    username: str


class UserResult(BaseModel):
    mongo_state: bool
    user_id: str
    username: str
    email: EmailStr


class GetUsersByName(BaseModel):
    usernames: List[str]


class GetLog(BaseModel):
    username: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    username: str | None = None
    email: str | None = None
    disabled: bool | None = None
