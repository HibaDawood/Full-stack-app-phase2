import requests
import os
from typing import Dict, Any

def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Mark a task as completed in the todo app
    
    Args:
        task_id (str): The ID of the task to mark as completed
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "https://hiba-05-todoapp-phase-2.hf.space")
    endpoint = f"{api_base_url}/api/v1/tasks/{task_id}"
    
    payload = {
        "status": "completed"
    }
    
    try:
        response = requests.put(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to complete task: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def mark_task_incomplete(task_id: str) -> Dict[str, Any]:
    """
    Mark a task as incomplete (pending) in the todo app
    
    Args:
        task_id (str): The ID of the task to mark as incomplete
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "https://hiba-05-todoapp-phase-2.hf.space")
    endpoint = f"{api_base_url}/api/v1/tasks/{task_id}"
    
    payload = {
        "status": "pending"
    }
    
    try:
        response = requests.put(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to mark task as incomplete: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Example usage
if __name__ == "__main__":
    # Example: Complete task with ID "some-task-id"
    result = complete_task("some-task-id")
    print("Complete task result:", result)
    
    # Example: Mark task as incomplete with ID "some-task-id"
    result = mark_task_incomplete("some-task-id")
    print("Mark incomplete result:", result)