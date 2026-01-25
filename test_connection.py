import requests

try:
    response = requests.get('http://0.0.0.0:8000/')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error connecting to server: {e}")