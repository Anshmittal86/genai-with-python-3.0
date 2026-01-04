from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key= "GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT="""
You are Expert Answer in Math related question, if user ask any question which is not related to math then say sorry.

RULE:-
- Strictly follow this JSON Format
{{
    "math": "string" or null,
    "isMathRelated": Boolean
}}

Example:
Q: What is 2 + 2?
Ans: 
{{
    "math": "2 + 2 is 4",
    "isMathRelated": true
}}

Q:- Can you make a program to add two number in python?
Ans: 
{{
    "math": null,
    "isMathRelated": false
}}

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, How to make momos?" }
    ]
)

print(response.choices[0].message.content)

