"""
This is a Python script for handling configuration settings using Pydantic.
It reads a JSON file and validates it against a predefined Pydantic model.
"""

import json
from enum import Enum
from pydantic_settings import BaseSettings


class HashingAlgorithmTypes(str, Enum):
    """Enum class for hashing algorithm types."""

    BCRYPT = "bcrypt"
    ARGON2 = "argon2"  # default


############################################################
########               JSON FORMAT                  ########
############################################################


class API_V1(BaseSettings):
    """
    Configuration settings for API version 1.

    Attributes:
        API_V1_ACTIVE (bool): Whether to use API version 1. Default is True.
        API_V1_ROUTE (str): The route for API version 1. Default is "/v1".
    """

    API_V1_ACTIVE: bool
    API_V1_ROUTE: str


class API_V2(BaseSettings):
    """
    Configuration settings for API version 2.

    Attributes:
        API_V2_ACTIVE (bool): Whether to use API version 2. Default is False.
        API_V2_ROUTE (str): The route for API version 2. Default is "/v2".
    """

    API_V2_ACTIVE: bool
    API_V2_ROUTE: str


class API(BaseSettings):
    """
    Configuration settings for the API.

    Attributes:
        API_ROUTE (str): The base route where the API is located. Default is "/api".
        API_V1 (API_V1): Configuration settings for API version 1.
        API_V2 (API_V2): Configuration settings for API version 2.
    """

    API_ROUTE: str
    API_V1: API_V1
    API_V2: API_V2


class BcryptHashingAlgorithm(BaseSettings):
    """
    Configuration settings for the Bcrypt password hashing algorithm.

    Attributes:
        ROUNDS (int): The number of rounds for Bcrypt. Default is 12.
        ENCODING (str): The character encoding used for hashing, e.g., 'utf-8'.
    """

    ROUNDS: int
    ENCODING: str


class ArgonHashingAlgorithm(BaseSettings):
    """
    Configuration settings for the Argon2 password hashing algorithm.

    Attributes:
        TIME_COST (int): The number of iterations (time cost) for Argon2. Default is 1048576 (2^20).
        MEMORY_COST (int): The memory usage (in MiB) for Argon2. Default is 65536 MiB.
        PARALLELISM (int): The number of threads (parallelism) used during Argon2 execution. Default is 4.
        HASH_LEN (int): The length of the resulting hash in bytes. Default is 16 bytes.
        SALT_LEN (int): The length of the salt used in bytes. Default is 32 bytes.
        ENCODING (str): The character encoding used for hashing, e.g., 'utf-8'.
    """

    TIME_COST: int
    MEMORY_COST: int
    PARALLELISM: int
    HASH_LEN: int
    SALT_LEN: int
    ENCODING: str


class PasswordConfig(BaseSettings):
    """
    Configuration settings for password hashing and password policies.

    Attributes:
        USE_PASSWORD_HASHING (bool): Whether to use password hashing.
        HASHING_ALGORITHM (HashingAlgorithmTypes): The selected password hashing algorithm.
        BcryptHashingAlgorithm (BcryptHashingAlgorithm): Configuration settings for Bcrypt.
        ArgonHashingAlgorithm (ArgonHashingAlgorithm): Configuration settings for Argon2.
        DEFAULT_PASSWORD_MIN_LENGTH (int): The default minimum password length. Default is 11.
        DEFAULT_PASSWORD_MAX_LENGTH (int): The default maximum password length. Default is 50.
    """

    USE_PASSWORD_HASHING: bool
    HASHING_ALGORITHM: HashingAlgorithmTypes
    BcryptHashingAlgorithm: BcryptHashingAlgorithm
    ArgonHashingAlgorithm: ArgonHashingAlgorithm
    DEFAULT_PASSWORD_MIN_LENGTH: int
    DEFAULT_PASSWORD_MAX_LENGTH: int


class MongodbSettings(BaseSettings):
    """
    Configuration settings for connecting to MongoDB.

    Attributes:
        MONGODB_HOST (str): The MongoDB host.
        MONGODB_PORT (int): The MongoDB port.
        DB_NAME (str): The name of the MongoDB database.
        MONGODB_USERNAME (str): Your MongoDB username (if required).
        MONGODB_PASSWORD (str): Your MongoDB password (if required).
        MONGODB_USE_SSL (bool): Whether to use SSL/TLS for communication.
        MONGODB_AUTH_MECHANISM (str): The authentication mechanism.
        MONGODB_MAX_POOL_SIZE (int): The maximum connection pool size.
        MONGODB_MIN_POOL_SIZE (int): The minimum connection pool size.
        MONGODB_MAX_IDLE_TIME_MS (int): The maximum time connections can remain idle.
        MONGODB_WAIT_QUEUE_TIMEOUT_MS (int): The wait queue timeout.
        MONGODB_SERVER_SELECTION_TIMEOUT_MS (int): The server selection timeout.
        MONGODB_READ_CONCERN (str): The read concern.
        MONGODB_WRITE_CONCERN (str): The write concern.
        MONGODB_RETRY_WRITES (bool): Whether to retry writes.
        MONGODB_CONNECT_TIMEOUT_MS (int): The connection timeout.
        MONGODB_SOCKET_TIMEOUT_MS (int): The socket timeout.
    """

    MONGODB_HOST: str
    MONGODB_PORT: int
    DB_NAME: str
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_USE_SSL: bool
    MONGODB_AUTH_MECHANISM: str
    MONGODB_MAX_POOL_SIZE: int
    MONGODB_MIN_POOL_SIZE: int
    MONGODB_MAX_IDLE_TIME_MS: int
    MONGODB_WAIT_QUEUE_TIMEOUT_MS: int
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int
    MONGODB_READ_CONCERN: str
    MONGODB_WRITE_CONCERN: str
    MONGODB_RETRY_WRITES: bool
    MONGODB_CONNECT_TIMEOUT_MS: int
    MONGODB_SOCKET_TIMEOUT_MS: int


class SessionManagerSettings(BaseSettings):
    """
    Configuration settings for the session manager.

    Attributes:
        ALLOW_COOKIE_LOGIN (bool): Allow login via the cookie field.
        DEFAULT_PATH (str): The default path for cookies.
        DEFAULT_STORE_IP_WITH_SESSION (bool): Store session with IP restriction.
        DEFAULT_MAX_NUMBER_OF_IPS (int): The number of allowed IPs per session.
        DEFAULT_DELETE_ON_LOGIN_ERROR (bool): Delete session on malicious login attempts.
        DEFAULT_MAX_AGE_SECONDS (int): The maximum age for a session in seconds. Default is 86400 (24 hours).
        DEFAULT_SECURE (bool): Whether the cookie should only be sent over HTTPS.
    """

    ALLOW_COOKIE_LOGIN: bool
    DEFAULT_PATH: str
    DEFAULT_STORE_IP_WITH_SESSION: bool
    DEFAULT_MAX_NUMBER_OF_IPS: int
    DEFAULT_DELETE_ON_LOGIN_ERROR: bool
    DEFAULT_MAX_AGE_SECONDS: int
    DEFAULT_SECURE: bool


class AppConfig(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        API (API): Configuration settings for the API.
        PasswordConfig (PasswordConfig): Configuration settings for password hashing and policies.
        MongodbSettings (MongodbSettings): Configuration settings for connecting to MongoDB.
        SessionManagerSettings (SessionManagerSettings): Configuration settings for the session manager.
    """

    API: API
    PasswordConfig: PasswordConfig
    MongodbSettings: MongodbSettings
    SessionManagerSettings: SessionManagerSettings


# Load JSON file
with open(
    R"C:\Users\user\Desktop\versioning_api_with_fastapi\config.json",
    encoding="utf-8",
) as f:
    config_data = json.load(f)

# Parse JSON into Pydantic model
config = AppConfig(**config_data)


# Validate the configuration data
