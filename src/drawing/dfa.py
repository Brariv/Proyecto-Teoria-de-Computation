from collections import deque
from graphviz import Digraph

def dfaToDiGraph(dfa_start):
    dot = Digraph(format='png')
    dot.attr('node', shape='circle')

    # BFS traversal to cover all DFA states
    queue = deque([dfa_start])
    seen = {dfa_start: "D0"}  # mapping DFAState -> label
    counter = 1

    while queue:
        current = queue.popleft()
        current_label = seen[current]
        
        # Add the node
        dot.node(current_label)

        # Add edges
        for symbol, next_state in current.edges.items():
            if next_state not in seen:
                seen[next_state] = f"D{counter}"
                counter += 1
                queue.append(next_state)
            dot.edge(current_label, seen[next_state], label=symbol)
    
    return dot
