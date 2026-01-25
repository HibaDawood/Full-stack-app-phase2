import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent / "backend"
sys.path.insert(0, str(project_root))

# Set environment variable for database
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'

# Import and run the app
import uvicorn
from src.main import app

print("Starting server on http://0.0.0.0:8000")
try:
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()