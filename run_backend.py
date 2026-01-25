#!/usr/bin/env python
import subprocess
import sys

def install_dependencies():
    """Install required packages"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_server():
    """Run the FastAPI server"""
    import uvicorn
    from src.main import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    print("Installing dependencies...")
    install_dependencies()
    print("Starting server...")
    run_server()