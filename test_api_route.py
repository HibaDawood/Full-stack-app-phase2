import subprocess
import json
import sys
import os

def test_api_route():
    """Test the API route by calling the Python script it points to"""
    print("Testing API route functionality...")
    
    # Test input
    test_input = json.dumps({"userInput": "Hello, how are you?"})
    
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
    print(f"Stderr: {result.stderr}")
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout.strip())
            print(f"Parsed response: {response}")
            return True
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return False
    else:
        print("Script execution failed")
        return False

if __name__ == "__main__":
    success = test_api_route()
    if success:
        print("\nSUCCESS: API route test passed!")
    else:
        print("\nFAILURE: API route test failed!")