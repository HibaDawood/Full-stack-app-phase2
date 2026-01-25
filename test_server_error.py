import subprocess
import time
import requests

# Start the server in the background
process = subprocess.Popen(['python', 'server.py'], cwd=r'C:\Users\hp\Desktop\hack-2-hb\phase-2\backend')

# Give the server some time to start
time.sleep(3)

try:
    # Make a request to trigger the error
    response = requests.get('http://0.0.0.0:8000/api/v1/tasks/')
    print(f"Response: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")

# Terminate the server
process.terminate()
process.wait()