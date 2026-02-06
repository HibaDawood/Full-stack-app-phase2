import requests
import json
from typing import Dict, Any

def delete_task(task_id: str) -> Dict[str, Any]:
    """
    Tool to delete a task via the backend API
    """
    try:
        # Assuming the backend is running on localhost:8000
        response = requests.delete(f"https://hiba-05-todoapp-phase-2.hf.space/api/v1/tasks/{task_id}")
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Task deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to delete task: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting task: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    result = delete_task("1")
    print(result)