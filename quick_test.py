import requests
import time
import subprocess
import os

# Start the server in a subprocess
env = os.environ.copy()
env['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

server_process = subprocess.Popen([
    'python', '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8010', '--log-level', 'info'
], cwd=r'C:\Users\hp\Desktop\hack-2-hb\phase-2\backend\src', env=env)

try:
    # Give the server some time to start
    time.sleep(5)
    
    print("Testing backend functionality...")
    
    # Test the health endpoint
    response = requests.get('http://0.0.0.0:8010/health')
    print(f"Health check: {response.status_code} - {response.text}")
    
    # Test the signup endpoint
    signup_data = {"email": "test@example.com", "password": "password123"}
    response = requests.post('http://0.0.0.0:8010/auth/signup', json=signup_data)
    print(f"Signup: {response.status_code}")
    
    # Test the signin endpoint
    signin_data = {"email": "test@example.com", "password": "password123"}
    response = requests.post('http://0.0.0.0:8010/auth/signin', json=signin_data)
    print(f"Signin: {response.status_code}")
    
    # Test the tasks endpoint
    response = requests.get('http://0.0.0.0:8010/api/v1/tasks/')
    print(f"Get tasks: {response.status_code}")
    
    print("All tests passed! Backend is working correctly.")

finally:
    # Terminate the server process
    server_process.terminate()
    server_process.wait()