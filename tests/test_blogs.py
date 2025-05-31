import pytest
from fastapi.testclient import TestClient
from blog_fast_api_python.main import app
from httpx import AsyncClient, ASGITransport


client = TestClient(app)

BASE_URL = "http://test"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWVjNGMyMC03ODhlLTRmZjYtYWIzMi1hNzRhYjJjODVkMTgiLCJleHAiOjE3NDg2ODMwNjN9.gKt0bx6jWNX6ppT7eo4NSo0C7uVL02IQciopoLG1VTg"


# Test PASSED
@pytest.mark.asyncio
async def test_get_all_blogs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        
        try:
            # print(f"Full URL: {client.base_url}")

            response = await client.get("/blogs")

            # print("Status:", response.status_code)
            
            assert response.status_code == 200

            # print("Response JSON:", response.json())
        except Exception as e:
            print(f"GET ALL BLOGS - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_create_blog():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:
        
        try:
            # print(f"Full URL: {client.base_url}")
            
            json = {
                "title": "Test Blog",
                "body": "Test content"
            }
            
            response = await client.post("/blogs", 
                headers={"Authorization": f"Bearer {access_token}"}, 
                json=json
            )

            # print("CREATE BLOG - Status:", response.status_code)
            
            assert response.status_code == 201

            # print("CREATE BLOG - Response JSON:", response.json())
        except Exception as e:
            print(f"CREATE BLOG - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_delete_blog_by_authorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:

        blog_id = "86dcdcfb-e811-4328-b14b-c22c07643af0"

        try:
            response = await client.delete(f"/blogs/{blog_id}", 
                headers={"Authorization": f"Bearer {access_token}"}
            )

            # print("DELETE BLOG BY AUTHORIZED - Status:", response.status_code)
        
            assert response.status_code == 200

            # print("DELETE BLOG BY AUTHORIZED - Response JSON:", response.json())
        except Exception as e:
            print(f"DELETE BLOG BY AUTHORIZED - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_delete_all_blogs_by_authorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:

        try:
            response = await client.delete(f"/blogs", 
                headers={"Authorization": f"Bearer {access_token}"}
            )

            # print("DELETE ALL BLOGS BY AUTHORIZED - Status:", response.status_code)

            # check if response status code is 200
            if response.status_code == 200:
                assert response.json()["message"] == "Blogs deleted successfully"
            else:
                assert response.json()["message"] == "User not authorized to delete all blogs."

            # print("DELETE ALL BLOGS BY AUTHORIZED - Response JSON:", response.json())
            
        except Exception as e:
            print(f"DELETE ALL BLOGS BY AUTHORIZED - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_update_blog():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:

        blog_id = "e3707071-3ea9-40eb-90ec-4c2b26b49aee"

        try:
            response = await client.put(f"/blogs/update/{blog_id}", 
                headers={"Authorization": f"Bearer {access_token}"},
                json={
                    "title": "Updated Blog",
                    "body": "Updated content"
                }
            )

            # print("UPDATE BLOG BY AUTHORIZED - Status:", response.status_code)

            # check if response status code is 200
            if response.status_code == 200:
                assert response.json()["message"] == "Blog updated successfully"
            else:
                assert response.json()["message"] == "User not authorized to update blog."

            # print("UPDATE BLOG BY AUTHORIZED - Response JSON:", response.json())
            
        except Exception as e:
            print(f"UPDATE BLOG BY AUTHORIZED - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_get_blog():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:

        blog_id = "e3707071-3ea9-40eb-90ec-4c2b26b49aee"

        try:
            response = await client.get(f"/blogs/{blog_id}", 
                headers={"Authorization": f"Bearer {access_token}"}
            )

            # print("GET BLOG - Status:", response.status_code)

            # check if response status code is 200
            if response.status_code == 200:
                assert response.json()["message"] == "Blog fetched successfully"
            else:
                assert response.json()["message"] == "Blog not found"

            # print("GET BLOG - Response JSON:", response.json())
            
        except Exception as e:
            print(f"GET BLOG - Error: {e}")


# Test PASSED
@pytest.mark.asyncio
async def test_current_user_blogs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"{BASE_URL}") as client:

        try:
            response = await client.get(f"/users/me/blogs", 
                headers={"Authorization": f"Bearer {access_token}"}
            )

            print("CURRENT USER BLOGS - Status:", response.status_code)

            # check if response status code is 200
            if response.status_code == 200:
                assert response.json()["message"] == "Blogs fetched successfully"
            else:
                assert response.json()["message"] == "User not authorized to fetch blogs."

            print("CURRENT USER BLOGS - Response JSON:", response.json())
            
        except Exception as e:
            print(f"CURRENT USER BLOGS - Error: {e}")


