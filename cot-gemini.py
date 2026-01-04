from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI(
    api_key= "AIzaSyC9-KUKavj-hKS4xTsvmkINcu7IDf5dHEA",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""
You're an expert AI Assistant in resolving user query using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT

Rules:- 
    - Strictly Follow the given JSON format
    - Very Very Strictly give me one step at a time and wait for the next step
    -  
    - The sequence of steps is START (Where user gives an input), PLAN (That can be multiple time) and finally OUTPUT (which is going to the displayed to the user.) 

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
Q: Hey, Can you solve 2 + 3 * 5 / 10?
Ans:
START: Hey, Can you solve 2 + 3 * 5 / 10?
PLAN: { "step": "PLAN", "content": "Seems, like user is interested in math problem." }
PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method." }
PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct think to done here." }
PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15." }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10." }
PLAN: { "step": "PLAN", "content": "Now , we must divide 15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "Now, the equation is 2 + 1.5" }
PLAN: { "step": "PLAN", "content": "Now, finally lets perform the addition on of 2 + 1.5 which is 3.5" }
PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as answer." }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, what is square root of 35" }
    ]
)

print(response.choices[0].message.content)



