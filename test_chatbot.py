import sys
import os
import json

# Add the mcp directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from mcp.gemini_agent import chat_with_gemini_agent

def test_agent():
    """Test the Gemini agent with various requests"""
    print("Testing Gemini Agent...")
    
    test_cases = [
        "Add a task to buy groceries",
        "Show me all tasks",
        "What is the weather today?",  # General query
        "Tell me a joke"  # General query
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case} ---")
        try:
            response = chat_with_gemini_agent(test_case)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_agent()