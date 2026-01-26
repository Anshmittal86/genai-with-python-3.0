from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated, Literal
from langgraph.types import Command
from dotenv import load_dotenv
load_dotenv()
import operator

class State(TypedDict):
    messages: Annotated[List[str], operator.add]

def node_a(state: State) -> Command[Literal["node_b", "node_c", END]]:
    print(f"\n\n\n Node A is receiving {state['messages']}")
    
    text = state['messages'][-1]
    if text == 'node_b':
        next_node = 'node_b'
    elif text == 'node_c':
        next_node = 'node_c'
    elif text == 'exit':
        next_node = END
    else:
        next_node = END
    
    return Command(
        update=State(messages=[text]),
        goto=[next_node]
    )

def node_b(state: State):
    print(f"\n\n\n Node B is receiving {state['messages']}")
    note = 'B'
    return State(messages=[note])

def node_c(state: State):
    print(f"\n\n\n Node C is receiving {state['messages']}")
    note = 'C'
    return State(messages=[note])


# Define a State   
graph_builder = StateGraph(State)

# Define a Node
graph_builder.add_node("node_a", node_a)
graph_builder.add_node("node_b", node_b)
graph_builder.add_node("node_c", node_c)

# Define a Edge
graph_builder.add_edge(START, "node_a")
graph_builder.add_edge("node_b", END)
graph_builder.add_edge("node_c", END)

graph = graph_builder.compile()
print(graph.get_graph().draw_mermaid())

while True:
    user = input('b, c or exit: ')
    print(user)
    input_state = State(messages=[user])
    result = graph.invoke(input_state)
    print(result)
    if result['messages'][-1] == 'exit':
        break