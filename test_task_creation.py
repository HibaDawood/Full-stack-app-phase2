import asyncio
import httpx
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_create_task():
    async with httpx.AsyncClient(base_url="http://0.0.0.0:8000") as client:
        try:
            response = await client.post(
                "/api/v1/tasks/",
                json={
                    "title": "Test Task",
                    "description": "Test Description",
                    "status": "pending"
                }
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_create_task())