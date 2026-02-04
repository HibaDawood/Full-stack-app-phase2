import requests
import json

# Test the chatbot API endpoint
def test_chatbot_api():
    url = "http://localhost:3000/api/agent"  # Assuming frontend runs on port 3000
    
    # Test data
    test_data = {
        "userInput": "Say hello"
    }
    
    try:
        response = requests.post(url, json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Chatbot API is working correctly!")
            return True
        else:
            print("[ERROR] Chatbot API returned an error")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the API. Make sure the frontend server is running on port 3000.")
        return False
    except Exception as e:
        print(f"[ERROR] Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing chatbot API endpoint...")
    test_chatbot_api()