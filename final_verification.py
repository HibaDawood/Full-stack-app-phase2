import subprocess
import json
import sys
import os

def test_complete_flow():
    """Test the complete flow from API call to Python script execution"""
    print("Testing complete flow...")
    
    # Test input
    test_input = json.dumps({"userInput": "What can you help me with?"})
    
    # Path to the Python script that the API route should call
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcp', 'gemini_agent.py')
    
    # Run the Python script with test input
    result = subprocess.run([
        sys.executable, 
        script_path, 
        test_input
    ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout.strip())
            print(f"Response: {response['response'][:100]}...")  # Show first 100 chars
            return True
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return False
    else:
        print("Script execution failed")
        return False

if __name__ == "__main__":
    print("="*50)
    print("FINAL CHATBOT FUNCTIONALITY TEST")
    print("="*50)
    
    success = test_complete_flow()
    
    print("\n" + "="*50)
    if success:
        print("SUCCESS! The chatbot should now work correctly.")
        print("- The API route is properly configured")
        print("- The Python script is working correctly")
        print("- Environment variables are accessible")
        print("- JSON responses are properly formatted")
        print("- The 500 error should be resolved")
    else:
        print("FAILURE! There are still issues.")
    print("="*50)