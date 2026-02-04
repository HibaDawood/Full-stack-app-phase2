import requests
import os
from typing import Dict, Any

def delete_task(task_id: str) -> Dict[str, Any]:
    """
    Delete a task from the todo app
    
    Args:
        task_id (str): The ID of the task to delete
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    endpoint = f"{api_base_url}/api/v1/tasks/{task_id}"
    
    try:
        response = requests.delete(endpoint)
        response.raise_for_status()
        
        # DELETE requests typically don't return JSON content
        if response.content:
            return response.json()
        else:
            return {"success": True, "message": f"Task {task_id} deleted successfully"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to delete task: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Example usage
if __name__ == "__main__":
    # Example: Delete task with ID "some-task-id"
    # NOTE: Be careful when running this as it will actually delete a task
    # result = delete_task("some-task-id")
    # print(result)
    print("Delete task function ready. Be careful when using this function.")