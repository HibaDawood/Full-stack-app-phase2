import os
import sys
import subprocess

# Try to run the server and capture output
result = subprocess.run([sys.executable, "-u", "server.py"], capture_output=True, text=True, timeout=30)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)