import requests
import json

# Base URL for the backend
BASE_URL = "https://hiba-05-todoapp-phase-2.hf.space"

def test_task_operations():
    print("Testing task operations...")
    
    # Step 1: Create a task
    print("\n1. Creating a new task...")
    create_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/tasks/", json=create_data)
    print(f"Create task response: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        print(f"Created task: {task}")
        task_id = task['id']
        
        # Step 2: Update the task
        print(f"\n2. Updating task with ID: {task_id}...")
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "completed"
        }
        
        response = requests.put(f"{BASE_URL}/api/v1/tasks/{task_id}", json=update_data)
        print(f"Update task response: {response.status_code}")
        if response.status_code == 200:
            updated_task = response.json()
            print(f"Updated task: {updated_task}")
        else:
            print(f"Failed to update task: {response.text}")
            
        # Step 3: Get the updated task
        print(f"\n3. Retrieving task with ID: {task_id}...")
        response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}")
        print(f"Get task response: {response.status_code}")
        if response.status_code == 200:
            retrieved_task = response.json()
            print(f"Retrieved task: {retrieved_task}")
        else:
            print(f"Failed to retrieve task: {response.text}")
    else:
        print(f"Failed to create task: {response.text}")

if __name__ == "__main__":
    test_task_operations()