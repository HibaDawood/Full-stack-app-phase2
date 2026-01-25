import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
os.environ.setdefault('BETTER_AUTH_SECRET', 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU')

def test_get_tasks():
    try:
        from backend.src.database import get_session
        from backend.src.api.v1.tasks import get_tasks
        from sqlmodel import Session
        
        # Create a session and call the function
        session_gen = get_session()
        session = next(session_gen)
        
        result = get_tasks(session=session)
        print(f"Success: {result}")
        
        # Close the session
        session.close()
    except Exception as e:
        print(f"Error in get_tasks: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_get_tasks()