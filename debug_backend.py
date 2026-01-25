import os
import sys
import traceback

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

try:
    print("Importing main app...")
    from backend.src.main import app
    print("Main app imported successfully")

    print("Importing auth router...")
    from backend.src.api.v1.auth import router as auth_router
    print("Auth router imported successfully")

    print("Importing tasks router...")
    from backend.src.api.v1.tasks import router as tasks_router
    print("Tasks router imported successfully")

    print("All imports successful, starting server...")
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")
except Exception as e:
    print("Error occurred:")
    traceback.print_exc()
    input("Press Enter to exit...")