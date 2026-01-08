from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

user_query = input("Bol Bhai: ")

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input="what is the weather of bijnor?"
)

print(response.output_text)