from graphviz import Digraph
from parsing.nfa import ThompsonsNFA as NFA, State

def addState(nfa_render:Digraph, visited:set[State], state:State, state_id:str, state_idx:int):
    if state not in visited:
        visited.add(state) # we add the state for not checking it again, in any case a klean operator does bad stuff

        # cause it is an imperative way of doing it, the state will be filled from the right states to the left ones
        if state.edge1 is None and state.edge2 is None:
            nfa_render.node(state_id, label=str(state_idx), shape="doublecircle")  # the double circle for the notation that bidkar uses
        else:
            nfa_render.node(state_id, label=str(state_idx))# puttin the emtpy string for it to not have a label
        

        if state.edge1: # Checking for existance
            nfa_render.edge(state_id, str(id(state.edge1)), label=state.label if state.label else "𝜀") # f**** hate this ascci not friendly epislon
        if state.edge2: # Checking for existance
            nfa_render.edge(state_id, str(id(state.edge2)), label="𝜀") # f**** hate this ascci not friendly epislon
 


# given our NFA, returns a graph for graphviz to parse it
def nfaToDiGraph(nfa: NFA):

    nfa_render:Digraph = Digraph() # where we render the things

    visited:set = set()

    state_idx:int = 0 # having the count of the state


    # we push to the stack the initial point of the nfa, and we start pushing to the stack all the subsecuent ones
    stack = [(nfa.initial, str(id(nfa.initial)))]

    while stack:
        state, state_id = stack.pop()

        state_idx += 1 
        
        addState(nfa_render, visited,state, state_id, state_idx)

        # we put both edges (with there respective state obviosly) for being check
        if state.edge1 and state.edge1 not in visited:
            stack.append((state.edge1, str(id(state.edge1))))
        if state.edge2 and state.edge2 not in visited:
            stack.append((state.edge2, str(id(state.edge2))))


    return nfa_render # just for doing the cool render


