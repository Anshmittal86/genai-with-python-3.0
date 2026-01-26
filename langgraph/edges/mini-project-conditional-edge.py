from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated, Literal
from langgraph.types import Command
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
import json

client = OpenAI()

class State(TypedDict):
    user_query: str
    is_coding_related: bool
    output_text: str

def is_coding(state: State) -> Command[Literal["coding_node", "chat_node", END]]:
    
    SYSTEM_PROMPT="""
    You are helpful AI Assistant. Your task is to solve user query. If user query related to coding then forward me to coding solving chat model by updating state.
    
    RULE:-
    - Strictly follow this JSON Format
    {
        'is_coding_related': boolean
    }
    
    Example:
    Q: What is 2 + 2?
    Answer: 
    { 'is_coding_related': False }
    
    Q: Can you give me a function to add two number in python?
    Answer: 
    { 'is_coding_related': True }
    
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
           { 'role': 'system', 'content': SYSTEM_PROMPT },
           { 'role': 'user', 'content': state['user_query'] }
        ]
    )
    
    parsed_result = json.loads(response.choices[0].message.content)
    
    if parsed_result.get('is_coding_related') == True:
        # call coding model 
        next_node = "coding_node"
    else:
        # call chat model
        next_node = "chat_node"
    return Command(
        update=State(is_coding_related=parsed_result.get('is_coding_related')),
        goto=[next_node]
    )

def coding_node(state: State):
    response = client.chat.completions.parse(
        model='gpt-5.2',
        messages=[
           { 'role': 'system', 'content': 'Your task is to solve your coding problem effectively' },
           { 'role': 'user', 'content': state['user_query'] }
        ]
    )

    return State(output_text=response.choices[0].message.content)

def chat_node(state: State):
    response = client.chat.completions.parse(
        model='gpt-4o-mini',
        messages=[
           { 'role': 'system', 'content': 'You are helpful AI Assistant. Your task is to solve user query.' },
           { 'role': 'user', 'content': state['user_query'] }
        ]
    )

    return State(output_text=response.choices[0].message.content)


# Define a State   
graph_builder = StateGraph(State)

# Define a Node
graph_builder.add_node("is_coding", is_coding)
graph_builder.add_node("coding_node", coding_node)
graph_builder.add_node("chat_node", chat_node)

# Define a Edge
graph_builder.add_edge(START, "is_coding")
graph_builder.add_edge("coding_node", END)
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()
# print(graph.get_graph().draw_mermaid())

while True:
    user = input('👨: ')
    
    if user == 'exit':
        break
    
    input_state = State(user_query=user)
    result = graph.invoke(input_state)
    
    
    print(f"🤖: {result}")
    