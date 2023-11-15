import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"msg": "Hello World"}

