import subprocess
import json
import os
from pathlib import Path

def test_api_route_path():
    """Test the API route path resolution as it would happen in Next.js"""
    print("Testing API route path resolution...")
    
    # Simulate the path resolution from the frontend API route
    # From frontend/src/app/api/agent/route.ts, process.cwd() would be the frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    # The path should be ../../../mcp/gemini_agent.py from the frontend directory perspective
    # But since we're running from the project root, we need to adjust
    
    # Calculate the path from the API route location:
    # API route is at: frontend/src/app/api/agent/route.ts
    # So from there, ../../../mcp/gemini_agent.py should lead to:
    # 1. ../ -> frontend/src/app/api
    # 2. ../ -> frontend/src/app  
    # 3. ../ -> frontend/src
    # 4. ../ -> frontend
    # 5. ../ -> project root
    # 6. mcp/gemini_agent.py -> project_root/mcp/gemini_agent.py
    
    # Actually, let's think differently:
    # From frontend/src/app/api/agent/, we go ../../.. to reach frontend/
    # Then from frontend/, we go ../mcp/gemini_agent.py to reach project_root/mcp/gemini_agent.py
    # So the path should be: ../mcp/gemini_agent.py from the frontend directory
    
    abs_script_path = Path(__file__).parent / "mcp" / "gemini_agent.py"
    
    print(f"Frontend directory: {frontend_dir}")
    print(f"Calculated script path: {abs_script_path}")
    print(f"Script exists: {abs_script_path.exists()}")
    
    # Test with a simple input
    test_input = json.dumps({"userInput": "Hi there!"})
    
    result = subprocess.run([
        "python", 
        str(abs_script_path),
        test_input
    ], capture_output=True, text=True, cwd=str(Path(__file__).parent))
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout.strip())
            print(f"Response received successfully: {len(response['response'])} chars")
            return True
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return False
    else:
        print("Script execution failed")
        return False

if __name__ == "__main__":
    success = test_api_route_path()
    if success:
        print("\nSUCCESS: API route path test passed!")
    else:
        print("\nFAILURE: API route path test failed!")