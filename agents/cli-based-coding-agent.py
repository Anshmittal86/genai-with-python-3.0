from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
import os
import subprocess

load_dotenv()

client = OpenAI()

class PermissionChecker:
    """Prompts for user confirmation before dangerous operations."""
    
    DANGEROUS_TOOLS = {
        'write_file': lambda input_json: f"Writing/Overwriting file: {json.loads(input_json).get('file_path', 'unknown')}",
        'run_shell': lambda cmd: f"Running shell command: {cmd[:100]}..."  # Truncate for display
    }
    
    @staticmethod
    def needs_permission(tool_name: str, tool_input: str) -> bool:
        return tool_name in PermissionChecker.DANGEROUS_TOOLS
    
    @staticmethod
    def get_description(tool_name: str, tool_input: str) -> str:
        if tool_name in PermissionChecker.DANGEROUS_TOOLS:
            return PermissionChecker.DANGEROUS_TOOLS[tool_name](tool_input)
        return ""
    
    @staticmethod
    def request_permission(tool_name: str, tool_input: str) -> bool:
        description = PermissionChecker.get_description(tool_name, tool_input)
        print(f"\n⚠️  PERMISSION REQUEST")
        print(f"Operation: {tool_name.upper()}")
        print(f"Details: {description}")
        print("-" * 50)
        response = input("Allow this operation? (y/n): ").strip().lower()
        print("-" * 50 + "\n")
        return response in ['y', 'yes']

def get_weather(city: str) -> str:
    print("🔨 Tool Called: get_weather, City: ", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}"
    return "Something went wrong"


def read_file(file_path: str)-> str:
    """ Reads the content of a file at the file path. """
    print("🔨 Tool Called: read_file: ", file_path)
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(input_json: str) -> str:
    print("🔨 Tool Called: write_file", input_json)
   
    file_params = json.loads(input_json)
   
    file_path = file_params.get("file_path")
    file_content = file_params.get("content")
   
    try:
        with open(file_path, 'w') as file:
            file.write(file_content)
        return f"✅ File written: {file_path}"
   
    except Exception as e:
        return f"Error Writing file: {str(e)}"
    
def safe_write_file(input_json: str) -> str:
    if PermissionChecker.request_permission('write_file', input_json):
        return write_file(input_json)  # Original function
    return "❌ Blocked by user: Write operation denied."


def list_directory(dir_path: str = ".") -> str:
    print("🔨 Tool Called: list_directory", dir_path)
    
    try:
        items = os.listdir(dir_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error Listing directory: {str(e)}"

def run_shell(cmd: str)-> str:
    print("🔨 Tool Called: run_shell", cmd)
   
    try:
        result = subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=30)
   
        output = result.stdout + result.stderr
        return f"Exit code {result.returncode}\nOutput: {output}"
   
    except subprocess.TimeoutExpired:
        return "Command Timed out"
    except Exception as e:
        return f"Error running command: {str(e)}"

def safe_run_shell(cmd: str) -> str:
    if PermissionChecker.request_permission('run_shell', cmd):
        return run_shell(cmd)  # Original function
    return "❌ Blocked by user: Shell command denied."
    

available_tool = {
    "get_weather": get_weather,
    "read_file": read_file,
    "write_file": safe_write_file,
    "list_directory": list_directory,
    "run_shell": safe_run_shell  
}

SYSTEM_PROMPT="""
You're an expert AI Assistant in resolving user query using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT
You can also access the tools to solve user query. If you need to access the tool so check the list of available tool and resolve the user query.

Available Tools:
- get_weather(city: str): Takes a city name as an input and returns the current weather for the city
- write_file(input_json: str): { "file_path": "file.py", "content": "code here" }
- list_directory(dir_path: str): Lists files in directory
- read_file(file_path: str): Reads content from file
- run_shell(cmd: str): Takes command as an input and run using subprocess module


Rules:- 
    - Strictly Follow the given JSON format
    - Only run one step at a time
    - The sequence of steps is START (Where user gives an input), PLAN (That can be multiple time), ACTION (function calling based on the user query), OBSERVE (understand the tool result) and finally OUTPUT (which is going to the displayed to the user.) 

Output JSON Format:
{ 
    "step": "START" | "PLAN" | "ACTION" | "OBSERVE" | "OUTPUT", 
    "content": "string"
    "tool": "The name of function if the step is action"
    "input": "the Input parameter for the function"
}

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

message_history=[
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👨: ")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=message_history
        )
        
        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result })
        
        parsed_result = json.loads(raw_result)
        
        step = parsed_result.get("step")
        content = parsed_result.get("content")
        
        if step == "START":
            print(f"🔥: {content}")
            continue
        
        if step == "PLAN":
            print(f"🧠: {content}")
            continue
        
        if step == "ACTION":
            tool_name = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"🔨: Tool name: {tool_name}, Input: {tool_input}")
            
            if tool_name in available_tool:
                if PermissionChecker.needs_permission(tool_name, tool_input):
                    pass
                
                tool_output = available_tool[tool_name](tool_input)
                print(f"🔨: Tool name: {tool_name}, Output: {tool_output}")
                
                message_history.append({ "role": "user", "content": json.dumps({ "step": "OBSERVE", "input": tool_input, "output": tool_output }) })
                continue

        if parsed_result.get("step") == "OUTPUT":
            print(f"🤖: {content}")
            break
        
    




