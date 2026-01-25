import os
from dotenv import load_dotenv
import traceback
import uvicorn
from src.main import app

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    print("Starting server on http://0.0.0.0:8000")
    print(f"Using database: {os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print(f"Server error: {e}")
        traceback.print_exc()