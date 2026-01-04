# THINKING...

# START: HEY, CAN YOU SOLVE 2 + 2
# ANALYSE ---> WHAT IS THAT?
# PLAN ---> MULTIPLE PLANING PHASE
# OUTPUT --> 4

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""
You're an expert AI Assistant in resolving user query using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT

Rules:- 
    - Strictly Follow the given JSON format
    - Only run one step at a time
    - The sequence of steps is START (Where user gives an input), PLAN(That can be multiple time) and finally OUTPUT (which is going to the displayed to the user.) 

"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Can You solve square root of 35" }
    ]
)

print(response.choices[0].message.content)



