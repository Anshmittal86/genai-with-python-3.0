from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
import operator

class State(TypedDict):
    messages: Annotated[List[str], operator.add]
    

def node_a(state: State):
    print(f"\n\n\n Node A is receiving {state['messages']}")
    note = 'A'
    return State(messages=[note])

def node_b(state: State):
    print(f"\n\n\n Node B is receiving {state['messages']}")
    note = 'B'
    return State(messages=[note])

def node_c(state: State):
    print(f"\n\n\n Node C is receiving {state['messages']}")
    note = 'C'
    return State(messages=[note])

def node_bb(state: State):
    print(f"\n\n\n Node BB is receiving {state['messages']}")
    note = 'BB'
    return State(messages=[note])

def node_cc(state: State):
    print(f"\n\n\n Node CC is receiving {state['messages']}")
    note = 'CC'
    return State(messages=[note])

def node_d(state: State):
    print(f"\n\n\n Node d is receiving {state['messages']}")
    note = 'D'
    return State(messages=[note])

# Define a State   
graph_builder = StateGraph(State)

# Define a Node
graph_builder.add_node("node_a", node_a)
graph_builder.add_node("node_b", node_b)
graph_builder.add_node("node_c", node_c)
graph_builder.add_node("node_bb", node_bb)
graph_builder.add_node("node_cc", node_cc)
graph_builder.add_node("node_d", node_d)

# Define a Edge
graph_builder.add_edge(START, "node_a")
graph_builder.add_edge("node_a", "node_b")
graph_builder.add_edge("node_a", "node_c")
graph_builder.add_edge("node_b", "node_bb")
graph_builder.add_edge("node_c", "node_cc")
graph_builder.add_edge("node_bb", "node_d")
graph_builder.add_edge("node_cc", "node_d")
graph_builder.add_edge("node_d", END)

graph = graph_builder.compile()
print(graph.get_graph().draw_mermaid())

initial_state = State(
    messages=["Hello world!"]  
)
updated_state = graph.invoke(initial_state)
print(updated_state)
