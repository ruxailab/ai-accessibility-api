import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemma-3n-e2b-it")

async def get_gemini_suggestion(input_data):
    prompt = f"""
You are an accessibility expert.

Element:
{input_data.element}

Issue:
{input_data.issue}

Help:
{input_data.help}

Provide a practical and helpful suggestion to improve this element.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
