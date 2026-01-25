import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Use SQLite instead of PostgreSQL to avoid dependency issues
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

def run_server():
    try:
        # Change to the backend directory and run it as a module
        import subprocess
        import sys

        # Set environment variables and run the backend module
        env = os.environ.copy()
        env['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
        env['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

        result = subprocess.run([
            sys.executable, "-m", "backend.src.main"
        ], env=env, cwd=project_root, shell=True)

        if result.returncode != 0:
            print(f"Backend exited with code: {result.returncode}")
        else:
            print("Backend shut down normally")

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server()