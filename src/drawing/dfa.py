from graphviz import Digraph
from collections import deque

def dfaToDiGraph(dfa_start):
    dot = Digraph(format='png')

    # BFS traversal to cover all DFA states
    queue = deque([dfa_start])
    seen = {dfa_start: "D0"}  # mapping DFAState -> label
    counter = 1
    all_states = []

    while queue:
        current = queue.popleft()
        current_label = seen[current]
        all_states.append(current)

        # Add edges
        for symbol, next_state in current.edges.items():
            if next_state not in seen:
                seen[next_state] = f"D{counter}"
                counter += 1
                queue.append(next_state)
            dot.edge(current_label, seen[next_state], label=symbol)

    # Now add nodes with correct shape (accepting states are doublecircle)
    for state in all_states:
        label = seen[state]
        # Accepting if any NFA state in this DFA state has no outgoing edges
        is_accepting = any(nfa_state.edge1 is None and nfa_state.edge2 is None for nfa_state, _ in state.nfa_states)
        shape = 'doublecircle' if is_accepting else 'circle'
        dot.node(label, shape=shape)

    return dot

