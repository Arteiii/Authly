"""
routes for different api versions
"""


from backend.authly.core.log import Logger
from backend.authly.api.api_v1.api import api_router as api_v1
from backend.authly.core.config import application_config
from backend.authly.core.config import LogLevel
from fastapi import APIRouter

API_ROUTE = application_config.API.API_ROUTE
API_V1 = application_config.API.API_V1
API_V2 = application_config.API.API_V2


api_main_router = APIRouter()


if (
    API_V1.API_V1_ACTIVE == API_V2.API_V2_ACTIVE
    and API_V1.API_V1_ROUTE == API_V2.API_V2_ROUTE
):
    Logger.log(LogLevel.CRITICAL, "Please fix API paths")

if API_V1.API_V1_ACTIVE is True:
    Logger.log(
        LogLevel.INFO,
        "api version 1 is available at:",
        f"        \\__ https://example.com{API_ROUTE}{API_V1.API_V1_ROUTE}",
    )
    api_main_router.include_router(api_v1, prefix=API_V1.API_V1_ROUTE)


# will add as soon as there is a version2
# if API_V2.API_V2_ACTIVE == True:
#     print(f"api version 2 is available at: {API_V2.API_V2_ROUTE}")
#     api_main_router.include_router(api_v2, prefix=API_V2.API_V2_ROUTE)
