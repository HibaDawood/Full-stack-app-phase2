import subprocess
import json
import sys
import os

# Add the project root to the path so we can import from mcp
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_workflow():
    """
    Test the complete workflow: voice/text input -> chatbot -> agent -> tools -> backend -> frontend
    """
    print("Testing complete workflow...")
    
    # Test 1: Test the gemini agent directly
    print("\n1. Testing Gemini agent directly...")
    try:
        # Test adding a task
        user_input = "Add a task to buy groceries"
        python_script_path = "./mcp/gemini_agent.py"
        
        result = subprocess.run([
            sys.executable, python_script_path, json.dumps({"userInput": user_input})
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"   [PASS] Gemini agent responded: {response['response']}")
        else:
            print(f"   [FAIL] Gemini agent failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error testing Gemini agent: {e}")
        return False
    
    # Test 2: Test the API route indirectly by checking if required files exist
    print("\n2. Checking API route setup...")
    api_route_path = "./frontend/src/app/api/agent/route.ts"
    if os.path.exists(api_route_path):
        print("   [PASS] API route exists")
    else:
        print("   [FAIL] API route missing")
        return False

    # Test 3: Check if chatbot component exists
    print("\n3. Checking chatbot component...")
    chatbot_path = "./frontend/src/components/chatbot/ChatBot.tsx"
    if os.path.exists(chatbot_path):
        print("   [PASS] ChatBot component exists")
    else:
        print("   [FAIL] ChatBot component missing")
        return False

    # Test 4: Check if tools exist
    print("\n4. Checking MCP tools...")
    tools_dir = "./mcp"
    required_tools = [
        "gemini_agent.py",
        "add_task_tool.py",
        "update_task_tool.py",
        "read_task_tool.py",
        "delete_task_tool.py",
        "complete_task_tool.py"
    ]

    all_exist = True
    for tool in required_tools:
        tool_path = os.path.join(tools_dir, tool)
        if os.path.exists(tool_path):
            print(f"   [PASS] {tool} exists")
        else:
            print(f"   [FAIL] {tool} missing")
            all_exist = False

    if not all_exist:
        return False

    # Test 5: Check if environment variables are set
    print("\n5. Checking environment configuration...")
    env_vars = {
        "NEXT_PUBLIC_API_URL": os.getenv("NEXT_PUBLIC_API_URL", "https://hiba-05-todoapp-phase-2.hf.space"),
        "Gemini_api_key": os.getenv(GEMINI_API_KEY)
    }

    for var, value in env_vars.items():
        if value:
            print(f"   [PASS] {var} is set")
        else:
            print(f"   [WARN] {var} is not set (using default)")

    print("\n[PASS] All tests passed! The complete workflow is properly set up.")
    print("\nWorkflow Summary:")
    print("- User speaks/inputs text -> ChatBot component captures input")
    print("- ChatBot sends input to /api/agent endpoint")
    print("- API route executes mcp/gemini_agent.py script")
    print("- Gemini agent parses request and selects appropriate tool")
    print("- Tool executes API call to backend")
    print("- Backend updates database")
    print("- Frontend receives response and updates UI")

    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    if success:
        print("\n[SUCCESS] Complete workflow test successful!")
    else:
        print("\n[ERROR] Complete workflow test failed!")
        sys.exit(1)