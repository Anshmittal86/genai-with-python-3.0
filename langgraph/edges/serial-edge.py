from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import List

class State(TypedDict):
    messages: List[str]
    
def node_a(state: State):
    
    print("\n\n\n Inside node_a: ", state)
    note="Hello world from Node a"
    
    return (State(messages = [note]))
    
# Create a state graph
graph_builder = StateGraph(State)

# Define a node
graph_builder.add_node("node_a", node_a)

# Define a Edges
graph_builder.add_edge(START, "node_a")
graph_builder.add_edge("node_a", END)

# Define a graph
graph = graph_builder.compile()

# print(graph.get_graph().draw_mermaid())

initial_state = State(
    messages=[
        "Hello Node a, how are you?"
    ]
)

updated_state = graph.invoke(initial_state)
print(updated_state)
    

