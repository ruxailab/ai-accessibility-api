
import google.generativeai as genai
genai.configure(api_key="AIzaSyC4gHKFDmDg1vmaGYUk6K4I6ajOMehPpAM")
model = genai.GenerativeModel('gemma-3n-e2b-it')
prompt = "is narendra modi a good pm"
try:
    response = model.generate_content(prompt)
    print("Gemini's response:")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your API key is correct and you have network connectivity.")
    print("You might also be exceeding rate limits or using a model that's not enabled.")
