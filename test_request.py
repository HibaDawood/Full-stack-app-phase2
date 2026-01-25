import requests
import time
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_api():
    url = "http://0.0.0.0:8000/api/v1/tasks/"
    data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending"
    }
    
    try:
        print("Attempting to create task...")
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 500:
            print("Error occurred - check server logs for details")
    except Exception as e:
        print(f"Request failed with error: {e}")

if __name__ == "__main__":
    # Give the server a moment to start
    time.sleep(2)
    test_api()