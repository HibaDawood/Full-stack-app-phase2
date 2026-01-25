#!/usr/bin/env python3
"""
Test script to debug the backend issue
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.main import app
import uvicorn
from src.database import engine
from sqlmodel import Session
from src.models.user import User
from src.models.task import Task, TaskCreate
from src.services.task_service import create_task
import uuid

def test_db_connection():
    """Test database connection"""
    try:
        with Session(engine) as session:
            # Try a simple query
            user_count = session.query(User).count()
            print(f"Connected to DB, user count: {user_count}")
            return True
    except Exception as e:
        print(f"DB connection failed: {e}")
        return False

def test_task_creation():
    """Test task creation logic directly"""
    try:
        # Create a mock user ID for testing
        mock_user_id = uuid.uuid4()
        
        # Create task data
        task_create = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="pending"
        )
        
        # Try to create task in a session
        with Session(engine) as session:
            db_task = create_task(
                session=session,
                task_create=task_create,
                user_id=mock_user_id
            )
            print(f"Task created successfully: {db_task.id}")
            return True
    except Exception as e:
        print(f"Task creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing backend components...")
    
    # Test DB connection
    if not test_db_connection():
        print("DB connection test failed")
        sys.exit(1)
    
    # Test task creation
    if not test_task_creation():
        print("Task creation test failed")
        sys.exit(1)
    
    print("All tests passed. Starting server...")
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")