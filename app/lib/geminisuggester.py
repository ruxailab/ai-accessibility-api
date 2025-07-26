import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

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
