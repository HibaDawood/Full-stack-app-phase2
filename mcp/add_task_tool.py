import requests
import os
from typing import Dict, Any

def add_task(title: str, description: str = "", status: str = "pending") -> Dict[str, Any]:
    """
    Add a new task to the todo app
    
    Args:
        title (str): The title of the task
        description (str): The description of the task
        status (str): The status of the task (pending, in-progress, completed)
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    endpoint = f"{api_base_url}/api/v1/tasks/"
    
    payload = {
        "title": title,
        "description": description,
        "status": status
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to add task: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Example usage
if __name__ == "__main__":
    result = add_task("Sample Task", "This is a sample task added via tool", "pending")
    print(result)