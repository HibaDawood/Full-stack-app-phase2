import os
import sys

# Add the backend/src directory to the Python path
sys.path.insert(0, './backend/src')

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require' 
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

try:
    # Import the app after setting environment variables
    from main import app
    import uvicorn
    
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()