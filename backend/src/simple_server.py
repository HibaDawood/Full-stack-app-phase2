import os
import sys

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

try:
    from main import app
    print('Successfully imported app')
    
    import uvicorn
    print('Successfully imported uvicorn')
    
    print('Starting server on http://0.0.0.0:8000...')
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()