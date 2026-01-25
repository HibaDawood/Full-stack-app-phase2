import requests
import time
import subprocess
import os
import json

# Start the server in a subprocess
env = os.environ.copy()
env['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

server_process = subprocess.Popen([
    'python', '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8008', '--log-level', 'info'
], cwd=r'C:\Users\hp\Desktop\hack-2-hb\phase-2\backend\src', env=env)

try:
    # Give the server some time to start
    time.sleep(5)
    
    # Test the health endpoint
    try:
        response = requests.get('http://127.0.0.1:8008/health')
        print(f"Health check response: {response.status_code}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
    except Exception as e:
        print(f"Error during health check: {e}")
    
    # Test the signup endpoint
    try:
        signup_data = {
            "email": "testuser@example.com",
            "password": "shortpass123"
        }
        response = requests.post('http://127.0.0.1:8008/auth/signup', json=signup_data)
        print(f"Signup response: {response.status_code}")
        print(f"Signup response content: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to signup endpoint")
    except Exception as e:
        print(f"Error during signup: {e}")

    # Test the signin endpoint
    try:
        signin_data = {
            "email": "testuser@example.com",
            "password": "shortpass123"
        }
        response = requests.post('http://127.0.0.1:8008/auth/signin', json=signin_data)
        print(f"Signin response: {response.status_code}")
        print(f"Signin response content: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to signin endpoint")
    except Exception as e:
        print(f"Error during signin: {e}")
        
    # Test the tasks endpoint
    try:
        response = requests.get('http://127.0.0.1:8008/api/v1/tasks/')
        print(f"Tasks response: {response.status_code}")
        print(f"Tasks response content: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to tasks endpoint")
    except Exception as e:
        print(f"Error during tasks: {e}")

finally:
    # Terminate the server process
    server_process.terminate()
    server_process.wait()