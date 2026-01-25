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
        
        # Get all users
        users = session.exec(select(User)).all()
        print(f"Number of users: {len(users)}")
        
        for i, user in enumerate(users):
            print(f"User {i}: ID={user.id}, Email={user.email}")
        
        # Get the first user to use as default
        if users:
            first_user = users[0]
            print(f"\nUsing first user as default: {first_user.id}")
        else:
            print("No users found in database")
    
except Exception as e:
    print(f"Query failed: {e}")
    import traceback
    traceback.print_exc()