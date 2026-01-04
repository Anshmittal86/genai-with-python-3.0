from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Prompting :- Instruction dene ka tarika
# Few shot :- Give Directly instruction to the model with few examples

SYSTEM_PROMPT="""
You are Expert Answer in Math related question, if user ask any question which is not related to math then say sorry.

Example:
Q: What is 2 + 2?
Ans: Hey, 2 + 2 is 4.

Q:- Can you make a program to add two number in python?
Ans: Sorry
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, How to make momos?" }
    ]
)

print(response.choices[0].message.content)

