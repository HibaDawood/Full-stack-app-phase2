from google import genai
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Get the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCH21tLcZZZV_mnfIEGhGNq-3uOQJxxm-g")

# Initialize the client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt: str, tools_info: str = "") -> str:
    """
    Get response from Gemini model
    """
    try:
        # Prepare the prompt with tools information if provided
        full_prompt = prompt
        if tools_info:
            full_prompt = f"{prompt}\n\nAvailable tools: {tools_info}"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text

    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"

def get_gemini_response_with_context(prompt: str, context: Dict[str, Any], tools_info: str = "") -> str:
    """
    Get response from Gemini model with additional context
    """
    try:
        # Prepare the prompt with context and tools information
        context_str = "\nContext: " + str(context) if context else ""
        tools_str = f"\n\nAvailable tools: {tools_info}" if tools_info else ""

        full_prompt = f"{prompt}{context_str}{tools_str}"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text

    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"

# Example usage
if __name__ == "__main__":
    response = get_gemini_response("Hello, how are you?")
    print(response)