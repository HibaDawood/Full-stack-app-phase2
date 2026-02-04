import requests
import json

# Test the chatbot API endpoint with various inputs
def test_chatbot_api():
    url = "http://localhost:3000/api/agent"  # Assuming frontend runs on port 3000
    
    test_cases = [
        {"userInput": "Say hello"},
        {"userInput": "Add a task to buy groceries"},
        {"userInput": "What can you help me with?"}
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_data['userInput']}")
        try:
            response = requests.post(url, json=test_data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("[SUCCESS] Chatbot API handled the request correctly!")
            else:
                print("[ERROR] Chatbot API returned an error")
                
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to the API. Make sure the frontend server is running on port 3000.")
            return False
        except Exception as e:
            print(f"[ERROR] Error occurred: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    print("Testing chatbot API endpoint with multiple inputs...")
    test_chatbot_api()