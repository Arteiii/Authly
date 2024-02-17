"""
routes for different api versions
"""

from fastapi import APIRouter

from authly.core.utils.log import Logger, LogLevel
from authly.core.config import application_config

# routes:
from authly.api.user.endpoint import user as user_router

API_CONFIG = application_config.API  # type: ignore

API_ROUTE = API_CONFIG.API_ROUTE
API_V1 = API_CONFIG.API_V1
API_V2 = API_CONFIG.API_V2


api_main_router = APIRouter()


def check_api_paths(f, s) -> bool:
    if f == s:
        return False
    return True


# if API_V1.API_V1_ACTIVE is True:
#     Logger.log(
#         LogLevel.INFO,
#         "api version 1 is available at:",
#         f"        \\__ https://example.com{API_ROUTE}{API_V1.API_V1_ROUTE}",
#     )
#     api_main_router.include_router(api_v1, prefix=API_V1.API_V1_ROUTE)

Logger.log(
    LogLevel.INFO,
    "API is available at:",
    f"        \\__ https://example.com{API_ROUTE}/",
)

api_main_router.include_router(user_router, prefix="/user")


@api_main_router.get("/")
async def api_main_router_hello_world():
    return {"msg": "Hello World"}


# will add as soon as there is a version2
# if API_V2.API_V2_ACTIVE == True:
#     print(f"api version 2 is available at: {API_V2.API_V2_ROUTE}")
#     api_main_router.include_router(api_v2, prefix=API_V2.API_V2_ROUTE)
