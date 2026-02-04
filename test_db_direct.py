import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, './backend')

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

from backend.src.database import get_session_context
from backend.src.models import UserOrm as User, TaskOrm as Task, UserCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import hashlib

def test_database_connection():
    print("Testing database connection and creating a task...")
    
    try:
        with get_session_context() as session:
            print("Connected to database successfully.")
            
            # Try to get or create a default user
            user = session.query(User).first()
            if not user:
                print("No user found, creating a default user...")
                default_email = "default@example.com"
                default_password = hashlib.sha256("default_password".encode()).hexdigest()
                user = User(email=default_email, password=default_password)
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"Created user with ID: {user.id}")
            
            # Create a test task
            print("Creating a test task...")
            task = Task(title="Test Task", description="This is a test task", status="pending", user_id=user.id)
            session.add(task)
            session.commit()
            session.refresh(task)
            print(f"Created task with ID: {task.id}")
            
            # Retrieve the task
            retrieved_task = session.query(Task).filter(Task.id == task.id).first()
            print(f"Retrieved task: {retrieved_task.title}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()