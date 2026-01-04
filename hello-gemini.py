from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key= "AIzaSyD7uGw3ZSSp42ptbMvy96QxYHwNWRKnFzU",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You name is Arush and you have tell chat with me in hienglish language." },
        { "role": "user", "content": "Kya haal chaal?" }
    ]
)

print(response.choices[0].message.content)

