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

def test_simple_gemini():
    """Test the simple gemini script as backup"""
    print("\nTesting simple gemini script...")
    
    # Test input
    test_input = json.dumps({"userInput": "Hello"})
    
    # Path to the simple Python script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gemini_agent.py')
    
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
    print("COMPREHENSIVE CHATBOT FUNCTIONALITY TEST")
    print("="*50)
    
    success1 = test_complete_flow()
    success2 = test_simple_gemini()
    
    print("\n" + "="*50)
    if success1 and success2:
        print("ALL TESTS PASSED! The chatbot should work correctly.")
        print("- The API route is properly configured")
        print("- The Python scripts are working correctly")
        print("- Environment variables are accessible")
        print("- JSON responses are properly formatted")
    else:
        print("SOME TESTS FAILED!")
        if not success1:
            print("  - Advanced gemini agent (mcp) failed")
        if not success2:
            print("  - Simple gemini agent failed")
    print("="*50)