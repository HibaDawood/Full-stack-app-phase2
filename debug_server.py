import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
os.environ.setdefault('BETTER_AUTH_SECRET', 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU')

try:
    from backend.src.main import app
    import uvicorn
    
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
except Exception as e:
    print(f"Error importing or starting app: {e}")
    import traceback
    traceback.print_exc()