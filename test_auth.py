import requests
import json

# Test signup
signup_data = {
    "email": "test@example.com",
    "password": "password123"
}

try:
    response = requests.post('http://0.0.0.0:8000/auth/signup', json=signup_data)
    print(f"Signup Status Code: {response.status_code}")
    print(f"Signup Response: {response.text}")
except Exception as e:
    print(f"Error during signup: {e}")

# Test signin
signin_data = {
    "email": "test@example.com",
    "password": "password123"
}

try:
    response = requests.post('http://0.0.0.0:8000/auth/signin', json=signin_data)
    print(f"\nSignin Status Code: {response.status_code}")
    print(f"Signin Response: {response.text}")
except Exception as e:
    print(f"Error during signin: {e}")