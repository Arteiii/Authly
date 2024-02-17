from typing import Annotated
from authly.crud import crud_admin
from authly.db.redis import RedisManager
from authly.models.admin_model import AdminAccount
from authly.security.authentication import token_module
from fastapi import Depends
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authly.core.utils import hashing


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/admin/token")


async def authenticate_user(user_data: OAuth2PasswordRequestForm) -> str:
    # TODO: add authenticate_user
    pass


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: add get_current_user
    pass
