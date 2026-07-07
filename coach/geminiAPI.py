import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def Ask_AI(prompt, team):
    api_key = os.environ.get("GEMINI_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Pikachu's coach brain requires a GEMINI_KEY or GEMINI_API_KEY environment variable to be set to analyze teams."
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt + " my team is " + team
        )
        return response.text
    except Exception as e:
        return f"Pikachu's brain is currently on high demand, please try again in a moment. Error: {str(e)}"
