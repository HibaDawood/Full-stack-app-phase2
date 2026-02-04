import requests
import json
from typing import Dict, Any

def add_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to add a new task via the backend API
    """
    try:
        # Assuming the backend is running on localhost:8000
        response = requests.post(
            "http://localhost:8000/api/v1/tasks",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Task added successfully",
                "task": response.json()
            }
        else:
            return {
                "success": False,
                "message": f"Failed to add task: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding task: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    sample_task = {
        "title": "Sample task from tool",
        "description": "Created via MCP tool",
        "status": "pending"
    }
    result = add_task(sample_task)
    print(result)