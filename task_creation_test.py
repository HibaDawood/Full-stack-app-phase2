import os
import uuid
from sqlmodel import SQLModel, create_engine, Session, select
from backend.src.models import Task, TaskCreate
from backend.src.database import database_url

print(f"Database URL: {database_url}")

try:
    engine = create_engine(database_url)
    print("Engine created successfully")
    
    with Session(engine) as session:
        print("Session created successfully")
        
        # Create a new task
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="pending"
        )
        
        # Create task with default user_id
        db_task = Task(
            **task_data.dict(),
            user_id=uuid.UUID("00000000-0000-0000-0000-000000000000")  # Default user ID as UUID
        )
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        print(f"Task created successfully with ID: {db_task.id}")
        
        # Query tasks to verify
        tasks = session.exec(select(Task)).all()
        print(f"Number of tasks after creation: {len(tasks)}")
        
    print("Task creation test completed successfully")
    
except Exception as e:
    print(f"Task creation failed: {e}")
    import traceback
    traceback.print_exc()