import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.environ.get("GEMINI_KEY")
client = genai.Client(api_key = api_key)


def Ask_AI(prompt, team):
  response = client.models.generate_content(model = 'gemini-3.5-flash', contents = prompt + "my team is" + team)
  return response.text
 


if __name__ == '__main__':
  print(Ask_AI('what do you think of my team', 'Blastoise, Kakuna, Squirtle, Nidoking'))
