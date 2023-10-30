"""
routes for different api versions
"""

import sys

from fastapi.logger import logger as fastapi_logger
from api.api_v1.api import api_router as api_v1
from core.config import config
from fastapi import APIRouter

API_ROUTE = config.API.API_ROUTE
API_V1 = config.API.API_V1
API_V2 = config.API.API_V2


api_main_router = APIRouter()


if (
    API_V1.API_V1_ACTIVE == API_V2.API_V2_ACTIVE
    and API_V1.API_V1_ROUTE == API_V2.API_V2_ROUTE
):
    fastapi_logger.critical("Please fix API paths")
    sys.exit(1)

if API_V1.API_V1_ACTIVE is True:
    print(
        f"api version 1 is available at:\n \\__\
            https://example.com{API_ROUTE}{API_V1.API_V1_ROUTE}"
    )
    api_main_router.include_router(api_v1, prefix=API_V1.API_V1_ROUTE)


# will add as soon as there is a version2
# if API_V2.API_V2_ACTIVE == True:
#     print(f"api version 2 is available at: {API_V2.API_V2_ROUTE}")
#     api_main_router.include_router(api_v2, prefix=API_V2.API_V2_ROUTE)
