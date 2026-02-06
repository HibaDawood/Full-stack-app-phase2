"""
Chat API for the Todo App backend
This adds the chat functionality directly to the main backend API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import sys
import os
import json
from typing import Dict, Any

router = APIRouter()

class ChatRequest(BaseModel):
    userInput: str

@router.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main endpoint to handle chat requests
    """
    try:
        # Execute the gemini_agent.py script with the user input
        # Look for the script in the backend directory (mcp folder)
        script_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mcp", "gemini_agent.py")

        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail=f"Agent script not found at {script_path}")

        # Execute the Python script and capture output
        result = subprocess.run([
            sys.executable,  # Use the same Python interpreter
            "-u",  # Unbuffered output
            script_path,
            json.dumps({"userInput": request.userInput})
        ], capture_output=True, text=True, timeout=60)  # 60-second timeout

        if result.returncode != 0:
            error_msg = result.stderr.strip()

            # Check for rate limiting errors
            if ('429' in error_msg or
                'rate limit' in error_msg.lower() or
                'quota' in error_msg.lower()):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )

            raise HTTPException(
                status_code=500,
                detail=f"Agent execution failed: {error_msg}"
            )

        # Parse the output from the script
        try:
            response_data = json.loads(result.stdout.strip())
            return response_data
        except json.JSONDecodeError:
            # If the output isn't valid JSON, return it as plain text
            return {"response": result.stdout.strip()}

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Request timeout: Agent took too long to respond"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )