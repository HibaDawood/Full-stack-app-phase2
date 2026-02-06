import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Get the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# Initialize the model
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(prompt: str, tools_info: str = "") -> str:
    """
    Get response from Gemini model
    """
    try:
        # Prepare the prompt with tools information if provided
        full_prompt = prompt
        if tools_info:
            full_prompt = f"{prompt}\n\nAvailable tools: {tools_info}"

        response = model.generate_content(full_prompt)
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

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"

import sys
import json

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            # Parse the input from command line
            input_data = json.loads(sys.argv[1])
            user_input = input_data.get('userInput', '')
            
            # Get response from Gemini
            response_text = get_gemini_response(user_input)
            
            # Return JSON response
            result = {"response": response_text}
            print(json.dumps(result))
        except Exception as e:
            error_result = {"error": f"Error processing request: {str(e)}"}
            print(json.dumps(error_result))
    else:
        response = get_gemini_response("Hello, how are you?")
        print(response)