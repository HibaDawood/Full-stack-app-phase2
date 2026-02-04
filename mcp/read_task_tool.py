import requests
import os
from typing import Dict, Any, List

def read_task(task_id: str = None) -> Dict[str, Any]:
    """
    Read tasks from the todo app
    
    Args:
        task_id (str): The ID of a specific task to read (optional). 
                      If not provided, returns all tasks
    
    Returns:
        Dict[str, Any]: Response from the API
    """
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "https://hiba-05-todoapp-phase-2.hf.space")
    
    if task_id:
        endpoint = f"{api_base_url}/api/v1/tasks/{task_id}"
    else:
        endpoint = f"{api_base_url}/api/v1/tasks/"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to read task(s): {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def read_all_tasks() -> List[Dict[str, Any]]:
    """
    Read all tasks from the todo app
    
    Returns:
        List[Dict[str, Any]]: List of all tasks
    """
    return read_task()

# Example usage
if __name__ == "__main__":
    # Read all tasks
    all_tasks = read_all_tasks()
    print("All tasks:", all_tasks)
    
    # Read a specific task (replace with actual task ID)
    # specific_task = read_task("some-task-id")
    # print("Specific task:", specific_task)