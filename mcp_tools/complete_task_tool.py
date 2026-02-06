import requests
import json
from typing import Dict, Any

def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Tool to mark a task as complete via the backend API
    """
    try:
        # Update the task status to 'completed'
        task_data = {"status": "completed"}
        
        response = requests.put(
            f"https://hiba-05-todoapp-phase-2.hf.space/api/v1/tasks/{task_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Task marked as completed successfully",
                "task": response.json()
            }
        else:
            return {
                "success": False,
                "message": f"Failed to complete task: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error completing task: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    result = complete_task("1")
    print(result)