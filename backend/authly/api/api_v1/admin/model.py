from pydantic import BaseModel, EmailStr, Field, constr, validator
from authly.api.api_v1.authentication import base64_password
from backend.authly.core.config import application_config

config_password_min_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH
)
config_password_max_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH
)


class AdminRegistration(BaseModel):
    email: EmailStr = Field(..., example="1337@Allah.com")
    username: str = Field(..., example="abc#1234")
    key: str = Field(
        ..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ=="
    )  # random generated key for onetime use if selfhost
    password: constr(
        min_length=config_password_min_length,
        max_length=config_password_max_length,
    ) = Field(..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ==")

    @validator("password")
    def validate_password(cls, value):
        return base64_password.validate_base64_password(value)

    def json(self, *args, **kwargs):
        self.password = base64_password.encode_to_base64(self.password)
        return dict(self)
