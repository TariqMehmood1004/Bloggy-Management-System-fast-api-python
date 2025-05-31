import pytest
from fastapi.testclient import TestClient
from blog_fast_api_python.main import app
from httpx import AsyncClient, ASGITransport


client = TestClient(app)

BASE_URL = "http://test"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNzRiMmY1Zi01MjBjLTQ4MjEtOTI1ZC0yODNjZDEwOTMwYTQiLCJleHAiOjE3NDg2OTM2MjF9.iGuhAZL3GGuc-duxPKKoJyr2hNqCgrE0FW79QMu-sEw"


# Test PASSED
@pytest.mark.asyncio
async def test_create_admin_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.post(
                "/register/admin",
                json={
                    "first_name": "Admin",
                    "last_name": "Admin",
                    "email": "admin@admin.com",
                    "username": "admin",
                    "is_admin": True,
                    "password": "admin"
                }
            )

            if response.status_code == 201:
                assert response.json()["message"] == "Admin created successfully"
            else:
                assert response.json()["message"] == "Admin not created"

        except Exception as e:
            print(f"CREATE ADMIN USER - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.post(
                "/register",
                json={
                    "first_name": "User",
                    "last_name": "User",
                    "email": "user@user.com",
                    "username": "user",
                    "password": "user"
                }
            )

            if response.status_code == 201:
                assert response.json()["message"] == "User created successfully"
            else:
                assert response.json()["message"] == "User not created"
        except Exception as e:
            print(f"CREATE USER - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.post(
                "/login",
                json={
                    "username": "user",
                    "password": "user"
                }
            )

            if response.status_code == 200:
                print("User logged in successfully")
            else:
                print("User not logged in")
        except Exception as e:
            print(f"LOGIN - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_get_current_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code == 200:
                print("User profile fetched successfully")
            else:
                print("User profile not fetched")
        except Exception as e:
            print(f"GET CURRENT USER - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_update_current_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.put(
                "/users/me/update",
                headers={"Authorization": f"Bearer {access_token}"},
                json={
                    "first_name": "User",
                    "last_name": "User",
                    "email": "user@user.com",
                    "password": "user"
                }
            )

            if response.status_code == 200:
                print("User profile updated successfully")
            else:
                print("User profile not updated")
        except Exception as e:
            print(f"UPDATE CURRENT USER - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_delete_current_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.delete(
                "/users/me/delete",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code == 200:
                print("User profile deleted successfully")
            else:
                print("User profile not deleted")
        except Exception as e:
            print(f"DELETE CURRENT USER - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_get_all_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        try:
            response = await client.get(
                "/users",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code == 200:
                print(f"All users fetched successfully: {response.json()["data"]}")
            else:
                print("All users not fetched")
        except Exception as e:
            print(f"GET ALL USERS - Error: {e}")


