import requests
import json
from typing import Dict, Any

def update_task(task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to update an existing task via the backend API
    """
    try:
        # Assuming the backend is running on localhost:8000
        response = requests.put(
            f"http://localhost:8000/api/v1/tasks/{task_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Task updated successfully",
                "task": response.json()
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update task: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating task: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    sample_update = {
        "title": "Updated task from tool",
        "description": "Updated via MCP tool",
        "status": "in_progress"
    }
    result = update_task("1", sample_update)
    print(result)