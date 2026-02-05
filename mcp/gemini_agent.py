import os
import sys
import json
try:
    from google.genai import Client
except ImportError as e:
    print(f"Google GenAI import error: {e}")
    # Fallback implementation or mock
    class MockClient:
        def __init__(self, api_key: str):
            self.models = MockModels()

    class MockModels:
        def generate_content(self, model, contents):
            # Simple mock response for testing purposes
            return MockResponse(contents)

    class MockResponse:
        def __init__(self, text):
            self.text = f"Mock response for: {text}"

    Client = MockClient
from typing import Dict, Any

# Add the project root to the path so we can import from mcp
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from add_task_tool import add_task
from update_task_tool import update_task
from read_task_tool import read_task, read_all_tasks
from delete_task_tool import delete_task
from complete_task_tool import complete_task, mark_task_incomplete

# Configure the Gemini API
GEMINI_API_KEY = "AIzaSyCH21tLcZZZV_mnfIEGhGNq-3uOQJxxm-g"
client = Client(api_key=GEMINI_API_KEY)

def parse_user_request(user_input: str) -> Dict[str, Any]:
    """
    Parse the user's request to determine the appropriate action and extract parameters.

    Args:
        user_input (str): The user's request

    Returns:
        Dict[str, Any]: A dictionary containing the action and parameters
    """
    # Construct the prompt for the Gemini model
    prompt = f"""
    Analyze the following user request and extract the intent and parameters:
    User request: "{user_input}"

    Possible intents:
    - add_task: User wants to add a new task
    - update_task: User wants to update an existing task
    - read_task: User wants to read a specific task or all tasks
    - delete_task: User wants to delete a task
    - complete_task: User wants to mark a task as completed
    - mark_task_incomplete: User wants to mark a task as incomplete
    - general_query: General question or request that doesn't fit the above categories

    For each intent, extract the relevant parameters:
    - add_task: title, description, status (default: "pending")
    - update_task: task_id, title (optional), description (optional), status (optional)
    - read_task: task_id (optional, if None then read all tasks)
    - delete_task: task_id
    - complete_task: task_id
    - mark_task_incomplete: task_id

    Respond in JSON format with the following structure:
    {{
        "action": "<intent>",
        "params": {{
            "param1": "value1",
            ...
        }}
    }}

    If the request is a general query, set action to "general_query" and params to an empty object.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        # Extract the JSON from the response
        response_text = response.text.strip()

        # Find the JSON part in the response (in case there's extra text)
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            return result
        else:
            # If no JSON found, return a general query
            return {"action": "general_query", "params": {}}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        if 'response' in locals():
            print(f"Response text: {response.text}")
        return {"action": "general_query", "params": {}}
    except Exception as e:
        # Check if it's a rate limiting error
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "rate-limits" in error_str:
            print(f"Rate limit error: {error_str}")
            # Return a general query to avoid JSON parsing issues
            return {"action": "general_query", "params": {"error": f"Rate limit exceeded: {error_str}"}}
        else:
            print(f"Error parsing user request: {e}")
            return {"action": "general_query", "params": {}}

def execute_action(action: str, params: Dict[str, Any]) -> str:
    """
    Execute the appropriate action based on the parsed request.

    Args:
        action (str): The action to execute
        params (Dict[str, Any]): Parameters for the action

    Returns:
        str: The result of the action
    """
    try:
        if action == "add_task":
            try:
                result = add_task(
                    title=params.get("title", ""),
                    description=params.get("description", ""),
                    status=params.get("status", "pending")
                )
                if "error" in result:
                    return f"Error adding task: {result['error']}"
                else:
                    return f"Task added successfully: {result.get('title', 'Untitled Task')}"
            except Exception as e:
                return f"Error adding task: {str(e)}"

        elif action == "update_task":
            try:
                task_id = params.get("task_id")
                title_to_find = params.get("title")  # This could be the title we're looking for

                # If task_id is not a valid UUID or numeric ID, try to find the task by title
                if task_id and not is_valid_task_id(task_id):
                    # Search for the task by title or description
                    all_tasks_result = read_all_tasks()
                    if "error" not in all_tasks_result and isinstance(all_tasks_result, list):
                        # Look for a task that matches the task_id (which might actually be a title)
                        matching_task = find_task_by_title_or_description(all_tasks_result, task_id)
                        if matching_task:
                            task_id = matching_task.get("id")
                        else:
                            # If no matching task is found using task_id, try using the title param if available
                            if title_to_find:
                                matching_task = find_task_by_title_or_description(all_tasks_result, title_to_find)
                                if matching_task:
                                    task_id = matching_task.get("id")

                            if not task_id or not matching_task:
                                # If no matching task is found, return an error message
                                search_term = task_id if not title_to_find else title_to_find
                                return f"Could not find a task with title or description containing '{search_term}'. Please check the task name or provide the task ID."
                elif not task_id and title_to_find:
                    # If no task_id was provided but we have a title, try to find the task by title
                    all_tasks_result = read_all_tasks()
                    if "error" not in all_tasks_result and isinstance(all_tasks_result, list):
                        matching_task = find_task_by_title_or_description(all_tasks_result, title_to_find)
                        if matching_task:
                            task_id = matching_task.get("id")
                        else:
                            return f"Could not find a task with title or description containing '{title_to_find}'. Please check the task name or provide the task ID."

                if not task_id:
                    return "No valid task ID provided. Please provide a task ID or a recognizable task title."

                result = update_task(
                    task_id=task_id,
                    title=params.get("title"),
                    description=params.get("description"),
                    status=params.get("status")
                )
                if "error" in result:
                    return f"Error updating task: {result['error']}"
                else:
                    return f"Task updated successfully: {result.get('title', 'Untitled Task')}"
            except Exception as e:
                return f"Error updating task: {str(e)}"

        elif action == "read_task":
            try:
                task_id = params.get("task_id")
                if task_id:
                    result = read_task(task_id)
                else:
                    result = read_all_tasks()

                if "error" in result:
                    return f"Error reading task(s): {result['error']}"
                else:
                    if isinstance(result, list):
                        if len(result) == 0:
                            return "No tasks found."
                        else:
                            task_list = "\n".join([f"- {task.get('title', 'Untitled Task')} (ID: {task.get('id', 'Unknown')})" for task in result])
                            return f"Tasks:\n{task_list}"
                    else:
                        return f"Task: {result.get('title', 'Untitled Task')} (Status: {result.get('status', 'Unknown')})"
            except Exception as e:
                return f"Error reading task(s): {str(e)}"

        elif action == "delete_task":
            try:
                task_id = params.get("task_id")

                # If task_id is not a valid UUID or numeric ID, try to find the task by title
                if task_id and not is_valid_task_id(task_id):
                    # Search for the task by title or description
                    all_tasks_result = read_all_tasks()
                    if "error" not in all_tasks_result and isinstance(all_tasks_result, list):
                        # Look for a task that matches the task_id (which might actually be a title)
                        matching_task = find_task_by_title_or_description(all_tasks_result, task_id)
                        if matching_task:
                            task_id = matching_task.get("id")
                        else:
                            # If no matching task is found using task_id, try to search among all tasks
                            # by treating the task_id as a potential title/description fragment
                            for task in all_tasks_result:
                                if task.get('title') and task_id.lower() in str(task.get('title', '')).lower():
                                    task_id = task.get('id')
                                    break
                                elif task.get('description') and task_id.lower() in str(task.get('description', '')).lower():
                                    task_id = task.get('id')
                                    break

                            if not task_id or task_id == params.get("task_id"):
                                # If still no matching task is found, return an error message
                                return f"Could not find a task with title or description containing '{task_id}'. Please check the task name or provide the task ID."

                if not task_id or (task_id == params.get("task_id") and not is_valid_task_id(task_id)):
                    return "No valid task ID provided. Please provide a task ID or a recognizable task title."

                result = delete_task(task_id)
                if "error" in result:
                    return f"Error deleting task: {result['error']}"
                else:
                    return f"Task deleted successfully."
            except Exception as e:
                return f"Error deleting task: {str(e)}"

        elif action == "complete_task":
            try:
                task_id = params.get("task_id")

                # If task_id is not a valid UUID or numeric ID, try to find the task by title
                if task_id and not is_valid_task_id(task_id):
                    # Search for the task by title or description
                    all_tasks_result = read_all_tasks()
                    if "error" not in all_tasks_result and isinstance(all_tasks_result, list):
                        # Look for a task that matches the task_id (which might actually be a title)
                        matching_task = find_task_by_title_or_description(all_tasks_result, task_id)
                        if matching_task:
                            task_id = matching_task.get("id")
                        else:
                            # If no matching task is found, return an error message
                            return f"Could not find a task with title or description containing '{task_id}'. Please check the task name or provide the task ID."

                if not task_id:
                    return "No valid task ID provided. Please provide a task ID or a recognizable task title."

                result = complete_task(task_id)
                if "error" in result:
                    return f"Error completing task: {result['error']}"
                else:
                    return f"Task marked as completed successfully."
            except Exception as e:
                return f"Error completing task: {str(e)}"

        elif action == "mark_task_incomplete":
            try:
                task_id = params.get("task_id")

                # If task_id is not a valid UUID or numeric ID, try to find the task by title
                if task_id and not is_valid_task_id(task_id):
                    # Search for the task by title or description
                    all_tasks_result = read_all_tasks()
                    if "error" not in all_tasks_result and isinstance(all_tasks_result, list):
                        # Look for a task that matches the title or description
                        matching_task = find_task_by_title_or_description(all_tasks_result, task_id)
                        if matching_task:
                            task_id = matching_task.get("id")
                        else:
                            # If no matching task is found, return an error message
                            return f"Could not find a task with title or description containing '{task_id}'. Please check the task name or provide the task ID."

                if not task_id:
                    return "No valid task ID provided. Please provide a task ID or a recognizable task title."

                result = mark_task_incomplete(task_id)
                if "error" in result:
                    return f"Error marking task as incomplete: {result['error']}"
                else:
                    return f"Task marked as incomplete successfully."
            except Exception as e:
                return f"Error marking task as incomplete: {str(e)}"

        elif action == "general_query":
            try:
                # For general queries, generate a response using Gemini
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                # Check if it's a rate limiting error
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "rate-limits" in error_str:
                    return f"Rate limit exceeded. Please try again later: {error_str}"
                else:
                    return f"Error processing general query: {str(e)}"

        else:
            return "I'm sorry, I didn't understand that request."
    except KeyError as e:
        return f"Missing required parameter: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def is_valid_task_id(task_id: str) -> bool:
    """
    Check if the provided task_id is a valid UUID or numeric ID.

    Args:
        task_id (str): The task ID to validate

    Returns:
        bool: True if the ID is valid, False otherwise
    """
    import re
    # Check if it's a UUID (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    # Check if it's a numeric ID
    numeric_pattern = re.compile(r'^\d+$')

    return bool(uuid_pattern.match(task_id) or numeric_pattern.match(task_id))


def find_task_by_title_or_description(tasks: list, search_term: str) -> dict:
    """
    Find a task by matching its title or description with the search term.

    Args:
        tasks (list): List of task dictionaries
        search_term (str): The term to search for in titles/descriptions

    Returns:
        dict: The matching task or None if not found
    """
    if not search_term:
        return None

    search_term_lower = search_term.lower()

    for task in tasks:
        # Handle cases where title or description might be None
        title = task.get('title') or ''
        description = task.get('description') or ''

        if search_term_lower in str(title).lower() or search_term_lower in str(description).lower():
            return task

    return None


def chat_with_gemini_agent(user_input: str) -> str:
    """
    Main function to process user input and return a response from the Gemini agent.

    Args:
        user_input (str): The user's input

    Returns:
        str: The response from the agent
    """
    # Parse the user's request
    parsed_request = parse_user_request(user_input)

    # Execute the appropriate action
    action = parsed_request["action"]
    params = parsed_request["params"]

    response = execute_action(action, params)

    return response

# Example usage
if __name__ == "__main__":
    import sys
    import json

    # Accept user input from command line argument
    if len(sys.argv) > 1:
        try:
            user_input = json.loads(sys.argv[1])['userInput']
            response = chat_with_gemini_agent(user_input)
            print(json.dumps({"response": response}))
        except Exception as e:
            # Ensure we always return valid JSON even if there's an error
            print(json.dumps({"response": f"Error processing request: {str(e)}"}))
    else:
        # Example user inputs
        examples = [
            "Add a task to buy groceries",
            "Show me all tasks",
            "Update task with ID 123 to have title 'Buy milk'",
            "Mark task 456 as completed",
            "Delete task 789",
            "Tell me a joke"
        ]

        for example in examples:
            print(f"\nUser: {example}")
            response = chat_with_gemini_agent(example)
            print(f"Agent: {response}")