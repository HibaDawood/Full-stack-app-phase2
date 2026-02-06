import requests
import time
import json

# Wait a moment for the server to start
time.sleep(3)

BASE_URL = "https://hiba-05-todoapp-phase-2.hf.space"

def test_task_operations():
    print("Testing task operations...")
    
    # Step 1: Create a task
    print("\n1. Creating a new task...")
    create_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "user_id": 1  # Using default user ID
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/tasks/", json=create_data)
        print(f"Create task response: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Created task: {json.dumps(task, indent=2)}")
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
                print(f"Updated task: {json.dumps(updated_task, indent=2)}")
            else:
                print(f"Failed to update task: {response.text}")
                
            # Step 3: Get the updated task
            print(f"\n3. Retrieving task with ID: {task_id}...")
            response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}")
            print(f"Get task response: {response.status_code}")
            if response.status_code == 200:
                retrieved_task = response.json()
                print(f"Retrieved task: {json.dumps(retrieved_task, indent=2)}")
            else:
                print(f"Failed to retrieve task: {response.text}")
                
            # Step 4: Delete the task
            print(f"\n4. Deleting task with ID: {task_id}...")
            response = requests.delete(f"{BASE_URL}/api/v1/tasks/{task_id}")
            print(f"Delete task response: {response.status_code}")
            if response.status_code == 200:
                print(f"Delete response: {response.json()}")
            else:
                print(f"Failed to delete task: {response.text}")
        else:
            print(f"Failed to create task: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_task_operations()