import os
from sqlmodel import SQLModel, create_engine, Session, select
from backend.src.models import Task, User
from backend.src.database import database_url

print(f"Database URL: {database_url}")

try:
    engine = create_engine(database_url)
    print("Engine created successfully")
    
    with Session(engine) as session:
        print("Session created successfully")
        
        # Try to query users
        users = session.exec(select(User)).all()
        print(f"Number of users: {len(users)}")
        
        # Try to query tasks
        tasks = session.exec(select(Task)).all()
        print(f"Number of tasks: {len(tasks)}")
        
    print("Database connection test completed successfully")
    
except Exception as e:
    print(f"Database connection failed: {e}")
    import traceback
    traceback.print_exc()