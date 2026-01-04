from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

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
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Can You solve square root of 35" }
    ]
)

print(response.choices[0].message.content)


