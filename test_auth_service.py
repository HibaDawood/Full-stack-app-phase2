import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

from backend.src.services.auth_service import create_user
from backend.src.database import engine
from sqlmodel import Session
from backend.src.schemas.auth import UserCreate

# Test creating a user
try:
    with Session(engine) as session:
        user_create = UserCreate(email="test@example.com", password="password123")
        user = create_user(session, user_create)
        print(f"User created successfully: {user.email}")
        print(f"User ID: {user.id}")
except Exception as e:
    print(f"Error creating user: {e}")
    import traceback
    traceback.print_exc()