import httpx
import pytest
from fastapi import status

valid_login_header: dict = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}

valid_login_data: dict = {
    "grant_type": "",
    "username": "Tester1@Authly-Test.com",
    "password": "a%5C%260%5D%23%25JEi7jh.N1MRg%7C%3F%3Dp1~",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}


@pytest.mark.asyncio
class TestCreateUser:
    async def test_invalid_data(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/user/", headers=valid_login_header, data=None
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_data(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/user/", headers=valid_login_header, data=valid_login_data
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestLogin:
    access_token: str

    async def test_valid_data(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/user/token",
            headers=valid_login_header,
            data=valid_login_data,
        )

        TestLogin.access_token = response.json().get("access_token")

        assert response.status_code == status.HTTP_200_OK

    async def test_invalid_data(self, test_client: httpx.AsyncClient):
        response = await test_client.post(
            "/api/v1/user/token", headers=valid_login_header, data=None
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


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
        invalid_headers: dict = valid_login_header
        invalid_headers.pop("Content-Type")
        response = await test_client.get(
            "/api/v1/user/me", headers=invalid_headers
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
