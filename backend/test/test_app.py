from authly.api import api_router
import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_api_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/api/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_api_v1_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/api/v1/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_api_v1_user_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/api/v1/user/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_activate_api():
    result = api_router.activate_api(
        "API_ROUTE",
        "API_V1.API_V1_ROUTE",
        "API_V1",
        api_router.api_v1,
        api_router.api_main_router,
    )
    assert result is True
