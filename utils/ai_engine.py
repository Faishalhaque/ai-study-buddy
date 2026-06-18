import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def initialize_ai():
    """Initializes the Gemini API using the environment variable."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return False, "⚠️ API Key is missing. Please add your GEMINI_API_KEY to the .env file."
        
    try:
        genai.configure(api_key=api_key)
        return True, "Success"
    except Exception as e:
        return False, f"Failed to configure AI: {str(e)}"

def get_gemini_response(prompt, context="", model_name="gemini-2.5-flash"):
    """
    Calls the Gemini API. 
    Strictly uses the requested model: gemini-2.5-flash
    """
    try:
        model = genai.GenerativeModel(model_name)

        if context:
            full_prompt = f"Study Material Context:\n{context}\n\nTask:\n{prompt}"
        else:
            full_prompt = prompt

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"Error connecting to AI ({model_name}): {str(e)}"
