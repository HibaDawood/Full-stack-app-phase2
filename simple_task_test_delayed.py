import requests
import time

# Give the server some time to start
time.sleep(3)

BASE_URL = "http://localhost:8005"

# Test creating a task
print("Creating a task...")

create_data = {
    "title": "Test Task",
    "description": "This is a test task",
    "status": "pending",
    "user_id": 1
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/tasks/", json=create_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code != 200:
        print("Headers:", response.headers)
except Exception as e:
    print(f"Error: {e}")

# Wait a bit more to see server logs
time.sleep(2)