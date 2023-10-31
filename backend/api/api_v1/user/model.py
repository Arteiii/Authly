import base64
from typing import Dict, Optional
from backend.core.log import Logger

from core.config import config
from core.password_validation import validate_password_complexity
from pydantic import BaseModel, EmailStr, Field, constr, validator


def encode_to_base64(value: str) -> str:
    try:
        encoded_password = base64.b64encode(value.encode()).decode()
        return encoded_password
    except Exception as e:
        raise ValueError(f"Error occurred while encoding to Base64: {e}")


def decode_base64(value: str) -> str:
    try:
        decoded_password = base64.b64decode(
            value.encode(), validate=True
        ).decode()
        return decoded_password
    except base64.binascii.Error as err:
        raise ValueError("Invalid Base64-encoded password") from err


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
        min_length=config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH,
        max_length=config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH,
    ) = Field(..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ==")

    @validator("password")
    def validate_password(cls, value):
        return validate_base64_password(value)

    def json(self, *args, **kwargs):
        self.password = encode_to_base64(self.password)
        return dict(self)



class Login(BaseModel):
    email: Optional[EmailStr]
    user_id: Optional[str]
    password: str

    @validator("password")
    def validate_password(cls, value):
        return decode_base64(value)


class UpdateUsername(BaseModel):
    user_id: str
    username: str


class UserResult(BaseModel):
    mongo_state: bool
    user_id: str
    username: str
    email: EmailStr


class GetUsersByName(BaseModel):
    usernames: list[str]


class GetLog(BaseModel):
    username: Optional[str]
