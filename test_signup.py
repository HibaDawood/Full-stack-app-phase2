import requests
import json

# Test the signup endpoint
url = "http://0.0.0.0:8000/auth/signup"
headers = {"Content-Type": "application/json"}
data = {"email": "test@example.com", "password": "password123"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")