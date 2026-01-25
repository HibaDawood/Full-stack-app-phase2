import os
import uvicorn
from src.main import app

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')
    
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug", reload=False)