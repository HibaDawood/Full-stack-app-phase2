import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

try:
    from main import app
    logger.info("Successfully imported app")
    
    import uvicorn
    logger.info("Successfully imported uvicorn")
    
    print("Starting server on http://0.0.0.0:8000...")
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
    
except Exception as e:
    logger.error(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()