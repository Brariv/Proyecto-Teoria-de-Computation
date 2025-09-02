from graphviz import Digraph
from collections import deque

def add_dfa_state(dfa_render, visited, state, state_id, state_idx):
    if state not in visited:
        visited.add(state)

        accepting_checks = []
        for nfa_state, _ in state.nfa_states:
            accepting_checks.append(nfa_state.edge1 is None and nfa_state.edge2 is None)

        is_accepting = any(accepting_checks)


        if is_accepting:
            dfa_render.node(state_id, label=str(state_idx), shape="doublecircle")
        else:
            dfa_render.node(state_id, label=str(state_idx), shape="circle")

        for symbol, next_state in state.edges.items():
            dfa_render.edge(state_id, str(id(next_state)), label=symbol)


def dfaToDiGraph(dfa_start):
    dfa_render: Digraph = Digraph(format='png')
    visited: set = set()
    state_idx: int = 0

    stack = [(dfa_start, str(id(dfa_start)))]

    while stack:
        state, state_id = stack.pop()
        state_idx += 1

        add_dfa_state(dfa_render, visited, state, state_id, state_idx)

        for next_state in state.edges.values():
            if next_state not in visited:
                stack.append((next_state, str(id(next_state))))

    return dfa_render

