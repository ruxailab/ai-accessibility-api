from ..lib.geminisuggester import get_gemini_suggestion

async def generate_gemini_suggestion(input_data):
    return await get_gemini_suggestion(input_data)
