import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="./backend/.env")

def run_server():
    try:
        # Change to the backend directory and run it as a module
        import subprocess
        import sys

        # Use the environment variables from .env file instead of hardcoded values
        env = os.environ.copy()

        result = subprocess.run([
            sys.executable, "-m", "uvicorn", "backend.src.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], env=env, cwd=Path(__file__).parent)

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
    print(f"Starting server with database: {os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'     )}")
    run_server()