from authly.core.config import application_config
from pydantic import BaseModel

config_password_min_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH
)
config_password_max_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH
)


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    username: str | None = None
    email: str | None = None
    disabled: bool | None = None


class UpdateUserEmail(BaseModel):
    oldEmail: str
    email: str
