from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key= "GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Prompting :- Instruction dene ka tarika
# Zero-shot :- Give Directly instruction to the model

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You are Expert Answer in Math related question, if user ask any question which is not related to math then say sorry." },
        { "role": "user", "content": "Hey, How to make momos?" }
    ]
)

print(response.choices[0].message.content)

