from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": "You name is Arush and you have tell chat with me in hienglish language." },
        { "role": "user", "content": "Kya haal chaal?" }
    ]
)

print(response.choices[0].message.content)

