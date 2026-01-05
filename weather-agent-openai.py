from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests

load_dotenv()

client = OpenAI()

def get_weather(city: str) -> str:
    print("🔨 Tool Called: get_weather, City: ", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}"
    return "Something went wrong"


available_tool = {
    "get_weather": get_weather
}


SYSTEM_PROMPT="""
You're an expert AI Assistant in resolving user query using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT
You can also access the tools to solve user query. If you need to access the tool so check the list of available tool and resolve the user query.

Available Tools:
- get_weather(city: str): Takes a city name as an input and returns the current weather for the city

Rules:- 
    - Strictly Follow the given JSON format
    - Only run one step at a time
    - The sequence of steps is START (Where user gives an input), PLAN (That can be multiple time), ACTION (function calling based on the user query), OBSERVE (understand the tool result) and finally OUTPUT (which is going to the displayed to the user.) 

Output JSON Format:
{ "step": "START" | "PLAN" | "ACTION" | "OBSERVE" | "OUTPUT", "content": "string" }

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

Example:
Q: What is the weather of goa?
Ans: 
START: What is the weather of goa?
PLAN: { "step": "PLAN", "content": "Seems, like user is interested in the weather report of the goa." }
PLAN: { "step": "PLAN", "content": "First I have to see the list of available tools to check that any tool available for solving the query." }
PLAN: { "step": "PLAN", "content": "Yes, We have a tool of get_weather to get the current info of weather based on city name." }
PLAN: { "step": "PLAN", "content": "Now, I have to check how many parameters it should accepts." }
PLAN: { "step": "PLAN", "content": "Ok the tool of get_weather accept only one parameter which is city name to find the latest weather report." }
PLAN: { "step": "ACTION", "tool": "get_weather", "input": "Goa" }
OBSERVE: { "step": "OBSERVE", "input": "Goa", "output": "the current weather of goa is 25 C" }
PLAN: { "step": "PLAN", "content": "ok, the current weather of goa is 25 C" }
OUTPUT: { "step": "OUTPUT", "content": "The weather of goa is 25 C" }
"""

class WeatherOutputSchema(BaseModel):
    step: str = Field(..., description="This is ID so that we can see what step ai will perform")
    content: Optional[str] = Field(None, description="this is output coming from ai")
    input: Optional[str] = Field(None, description="this is the input of the function coming from ai")
    output: Optional[str] = Field(None, description="this is the tool output for ai understanding")
    tool: Optional[str] = Field(None, description="this is the function name")

message_history=[
    { "role": "system", "content": SYSTEM_PROMPT },
]

user_query = input("👨: ")
message_history.append({ "role": "user", "content": user_query })

while True:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=WeatherOutputSchema,
        messages=message_history
    )
    
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result })
    
    parsed_result = response.choices[0].message.parsed
    
    if parsed_result.step == "START":
        print(f"🔥: {parsed_result.content}")
        continue
    
    if parsed_result.step == "PLAN":
        print(f"🧠: {parsed_result.content}")
        continue
    
    if parsed_result.step == "ACTION":
        tool_name = parsed_result.tool
        tool_input = parsed_result.input
        print(f"🔨: Tool name: {tool_name}, Input: {tool_input}")
        
        if tool_name in available_tool:
            tool_output = available_tool[tool_name](tool_input)
            print(f"🔨: Tool name: {tool_name}, Output: {tool_output}")
            
            message_history.append({ "role": "user", "content": json.dumps({ "step": "OBSERVE", "input": tool_input, "output": tool_output }) })
            continue

    if parsed_result.step == "OUTPUT":
        print(f"🤖: {parsed_result.content}")
        break
    
    




