from authly.api.api_v1 import exceptions
import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
class TestCreateUser:
    async def test_invalid_data(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "",
            "username": "InvalidTester1@Authly-Test.com",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }

        response = await test_client.post(
            "/api/v1/user/", headers=headers, data=data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_data(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "",
            "username": "Tester1@Authly-Test.com",
            "password": "a%5C%260%5D%23%25JEi7jh.N1MRg%7C%3F%3Dp1~",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }

        response = await test_client.post(
            "/api/v1/user/", headers=headers, data=data
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestLogin:
    access_token: str

    async def test_valid_data(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "",
            "username": "Tester1@Authly-Test.com",
            "password": "a%5C%260%5D%23%25JEi7jh.N1MRg%7C%3F%3Dp1~",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }

        response = await test_client.post(
            "/api/v1/user/token", headers=headers, data=data
        )

        TestLogin.access_token = response.json().get("access_token")

        assert response.status_code == status.HTTP_200_OK

    async def test_invalid_data(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "",
            "username": "InvalidTester1@Authly-Test.com",
            "password": "a%5C%20%5D%.N1M%3F%3Dp1~",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }

        response = await test_client.post(
            "/api/v1/user/token", headers=headers, data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
class TestUserOperations:
    async def test_users_me(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TestLogin.access_token}",
        }

        response = await test_client.get("/api/v1/user/me", headers=headers)

        assert response.status_code == status.HTTP_200_OK

    async def test_users_me_invalid(self, test_client: httpx.AsyncClient):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer saoihasdaspodasdnoiashd",
        }

        response = await test_client.get("/api/v1/user/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
