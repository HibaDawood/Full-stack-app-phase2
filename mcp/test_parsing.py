import json
import sys
import os

# Add the project root to the path so we can import from mcp
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_agent import parse_user_request

# Test the parsing function
test_inputs = [
    "Update task with title 'buy groceries' to have status 'completed'",
    "Edit task buy groceries to mark as completed",
    "Update task hello to have status completed",
    "Delete task hello"
]

for test_input in test_inputs:
    print(f"\nInput: {test_input}")
    result = parse_user_request(test_input)
    print(f"Parsed result: {json.dumps(result, indent=2)}")