import asyncio
from asgi_lifespan import LifespanManager
from authly.app import app
import httpx
import pytest
import pytest_asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://app.io"
        ) as test_client:
            yield test_client
