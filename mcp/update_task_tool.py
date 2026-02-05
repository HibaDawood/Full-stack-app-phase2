import requests
import os
from typing import Dict, Any

def update_task(task_id: str, title: str = None, description: str = None, status: str = None) -> Dict[str, Any]:
    """
    Update an existing task in the todo app
    
    Args:
        task_id (str): The ID of the task to update
        title (str): The new title of the task (optional)
        description (str): The new description of the task (optional)
        status (str): The new status of the task (optional)
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    endpoint = f"{api_base_url}/api/v1/tasks/{task_id}"
    
    payload = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    
    try:
        response = requests.put(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to update task: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Example usage
if __name__ == "__main__":
    # Example: Update task with ID "some-task-id"
    result = update_task("some-task-id", title="Updated Task Title", status="in-progress")
    print(result)