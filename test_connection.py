import requests
import traceback

BASE_URL = "http://localhost:8000"

def test_connection():
    try:
        print("Attempting to connect to server...")
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Other error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()