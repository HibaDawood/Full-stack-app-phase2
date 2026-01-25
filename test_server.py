import requests
import time
import subprocess
import os

# Start the server in a subprocess
env = os.environ.copy()
env['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

server_process = subprocess.Popen([
    'python', '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8007', '--log-level', 'info'
], cwd=r'C:\Users\hp\Desktop\hack-2-hb\phase-2\backend\src', env=env)

try:
    # Give the server some time to start
    time.sleep(5)
    
    # Test the health endpoint
    try:
        response = requests.get('http://127.0.0.1:8007/health')
        print(f"Health check response: {response.status_code}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
    except Exception as e:
        print(f"Error during health check: {e}")
        
finally:
    # Terminate the server process
    server_process.terminate()
    server_process.wait()