import sys
import os
sys.path.insert(0, '.')

# Use SQLite instead of PostgreSQL to avoid dependency issues
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

import main
import uvicorn

print("Starting server on http://0.0.0.0:8000...")
uvicorn.run(main.app, host='0.0.0.0', port=8000, log_level='info')