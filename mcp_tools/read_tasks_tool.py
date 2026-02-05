import requests
import json
from typing import Dict, Any

def read_tasks(filters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Tool to read tasks via the backend API
    """
    try:
        # Assuming the backend is running on localhost:8000
        url = "http://localhost:8000/api/v1/tasks"
        if filters:
            # Convert filters to query parameters
            query_params = "&".join([f"{k}={v}" for k, v in filters.items()])
            url += f"?{query_params}"
            
        response = requests.get(url)
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Tasks retrieved successfully",
                "tasks": response.json()
            }
        else:
            return {
                "success": False,
                "message": f"Failed to retrieve tasks: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving tasks: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    result = read_tasks({"status": "pending"})
    print(result)