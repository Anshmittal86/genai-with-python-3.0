from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import List, Annotated
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()
import operator

class State(TypedDict):
    messages: Annotated[List[str], operator.add]
    
llm = init_chat_model(
    model='gpt-4o-mini',
    model_provider='openai'
)


def node_a(state: State):
    print(f"\n\n\n Node a is receiving {state['messages']}")
    
    response = llm.invoke(state["messages"])
    return State(messages=[response.content])

def node_b(state: State):
    print(f"\n\n\n Node b is receiving {state['messages']}")
    response = llm.invoke(state["messages"])
    return State(messages=[response.content])

# Define a state 
graph_builder = StateGraph(State)

# Define a node
graph_builder.add_node("node_a", node_a)
graph_builder.add_node("node_b", node_b)

# Define a edges
graph_builder.add_edge(START, "node_a")
graph_builder.add_edge(START, "node_b")
graph_builder.add_edge("node_a", END)
graph_builder.add_edge("node_b", END)

# compile a graph
graph = graph_builder.compile()

# print(graph.get_graph().draw_mermaid())
initial_state = State(
    messages=["Hello world!"]
)

updated_state = graph.invoke(initial_state)
print(updated_state)


# ["Hello world!"]
# START -> ["Hello world!"]
# node_a -> ["Hello world!", 'A']
# node_b -> ["Hello world!", 'A', 'B']
# END -> ["Hello world!", 'A', 'B']
# ["Hello world!", 'A', 'B']