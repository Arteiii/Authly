"""
routes for different api versions
"""


import sys
from backend.authly.core.log import Logger, LogLevel
from backend.authly.api.api_v1.api import api_router as api_v1
from backend.authly.core.config import application_config
from fastapi import APIRouter

API_CONFIG = application_config.API  # type: ignore

API_ROUTE = API_CONFIG.API_ROUTE
API_V1 = API_CONFIG.API_V1
API_V2 = API_CONFIG.API_V2


api_main_router = APIRouter()


def check_api_paths(f, s) -> bool:
    if f == s:
        return False
    return True


def activate_api(
    main_path: str,
    api_route: str,
    api_version: str,
    api: APIRouter,
    main_router: APIRouter,
) -> bool:
    Logger.log(
        LogLevel.INFO,
        f"api ({api_version}) is available at:",
        f"        \\__ https://example.com{main_path}{api_route}",
    )
    main_router.include_router(api, prefix=api_route)
    return True


def main(stop: bool = False):
    if stop:
        sys.exit()

    activate_api(
        API_ROUTE, API_V1.API_V1_ROUTE, "API_V1", api_v1, api_main_router
    )


main(check_api_paths(API_V1.API_V1_ROUTE, API_V2.API_V2_ROUTE))


@api_main_router.get("/")
async def api_main_router_hello_world():
    return {"msg": "Hello World"}


# will add as soon as there is a version2
# if API_V2.API_V2_ACTIVE == True:
#     print(f"api version 2 is available at: {API_V2.API_V2_ROUTE}")
#     api_main_router.include_router(api_v2, prefix=API_V2.API_V2_ROUTE)
