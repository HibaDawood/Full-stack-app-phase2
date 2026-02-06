import subprocess
import json
import sys
import os

# Add the project root to the Python path so we can import modules
sys.path.insert(0, os.path.abspath('.'))

def test_python_script():
    """Test the Python script directly"""
    print("Testing Python script...")
    
    # Test input
    test_input = json.dumps({"userInput": "Hello, how are you?"})
    
    # Run the Python script with test input
    result = subprocess.run([
        sys.executable, 
        'gemini_agent.py', 
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
    success = test_python_script()
    if success:
        print("\nSUCCESS: Python script test passed!")
    else:
        print("\nFAILURE: Python script test failed!")