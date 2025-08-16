from graphviz import Digraph
from parsing.nfa import NFA

def add_state(nfa_render, visited, state, state_id):
    if state not in visited:
        visited.add(state) # we add the state for not checking it again, in any case a klean operator does bad stuff
        nfa_render.node(state_id, label=str()) # puttin the emtpy string for it to not have a label 
        
        if state.edge1: # Checking for existance
            nfa_render.edge(state_id, str(id(state.edge1)), label=state.label if state.label else "E") # the one and only, friendly utf-8 epsilon
        if state.edge2: # Checking for existance
            nfa_render.edge(state_id, str(id(state.edge2)), label="E") # the one and only, friendly utf-8 epsilon



# given our NFA, retunrs a graph for graphviz to parse it
def nfaToDiGraph(nfa: NFA):
    nfa_render:Digraph = Digraph() # where we render the things
    visited:set = set()

    # we push to the stack the initial point of the nfa, and we start pushing to the stack all the subsecuent ones
    stack = [(nfa.initial, str(id(nfa.initial)))]

    while stack:
        state, state_id = stack.pop()
        add_state(nfa_render, visited,state, state_id)

        # we put both edges (with there respective state obviosly) for being check
        if state.edge1 and state.edge1 not in visited:
            stack.append((state.edge1, str(id(state.edge1))))
        if state.edge2 and state.edge2 not in visited:
            stack.append((state.edge2, str(id(state.edge2))))


    return nfa_render # just for doing the cool render


