from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define your tools
@tool
def get_weather(city: str) -> str:
    """ This function takes a city name and get a current weather of the city. """
    print("🔨 Tool Called: get_weather, City: ", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}"
    return "Something went wrong"

@tool
def calculator(expression: str) -> str:
    """
    This function takes a mathematical expression as a string
    and returns the calculated result.
    Example: "12 * (5 + 3)"
    """
    print("🔨 Tool Called: calculator, Expression:", expression)

    try:
        # WARNING: eval is used intentionally for controlled tool input
        result = eval(expression, {"__builtins__": {}})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
    
@tool
def read_file(file_path: str) -> str:
    """
    This function reads the content of a text file
    and returns it as a string.
    """
    print("🔨 Tool Called: read_file, Path:", file_path)

    try:
        if not os.path.exists(file_path):
            return "File not found"

        if not os.path.isfile(file_path):
            return "Path is not a file"

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            return "File is empty"

        return content

    except Exception as e:
        return f"File read error: {str(e)}"

tools = [get_weather, calculator, read_file]

# 2. Initialize the LLM
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2, 
    max_tokens=200,
    timeout=30
)

# 3. Create the agent
agent = create_agent(model, tools=tools)

# 4. invoke the agent
user_query = input("👨: ")
result = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})

print(result['messages'][-1].content)