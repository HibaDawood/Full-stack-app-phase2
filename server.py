import os
import sys
import uvicorn

# Add the project root directory to the Python path
sys.path.insert(0, './backend')

from src.main import app

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
    os.environ.setdefault('BETTER_AUTH_SECRET', 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU')

    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")