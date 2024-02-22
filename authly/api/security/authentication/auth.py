from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from authly.db.mongo import MongoDBManager

from authly.db.redis import RedisManager
from authly.api.security.authentication import token_module
from authly.core.utils import hashing
from authly.api.user import model
from authly.api.user import user as userManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


class TokenModel(BaseModel):
    access_token: str
    token_type: str


async def authenticate_user(
    user_data: OAuth2PasswordRequestForm, mongo_client: MongoDBManager
) -> str:
    try:
        success, data, details = await userManager.get_user_data_by_email(
            user_data.username, mongo_client
        )

        user = model.User(**data)

        if not hashing.verify_password(user_data.password, user.password):
            raise ValidationException("invalid password")

        redis_manager = RedisManager(redis_db=1)
        redis_manager.connect()

        new_token = token_module.get_new_token(
            str(data.id), redis_manager
        )  # TODO: test with redis active

    except ValueError:
        raise
    except ValidationException:
        raise
    except Exception:
        raise

    else:
        return new_token

    finally:
        redis_manager.close()


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> str:
    redis_manager = RedisManager()
    try:
        redis_manager.connect()
        user_id = token_module.get_user_id(token, redis_manager)

    except Exception:
        raise ValidationException("invalid token")

    else:
        return user_id

    finally:
        redis_manager.close()
