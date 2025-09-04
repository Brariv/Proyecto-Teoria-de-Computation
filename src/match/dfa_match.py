from parsing.dfa import State as DFAState

def matchStringToDfa(dfa:DFAState, string:str) -> bool:

    current = dfa  # The current state

    # Loop through each character in the string
    for s in string:

        # Checks the edges of the state for the character
        if s in current.edges:

            # we add the next state to be checked
            current = current.edges[s]

        # If there is no edge for the character, the string is not accepted
        else: 
            return False

    # Check if the last state is an accept state
    for nfa_state, _ in current.closure:
        # if the NFA of the DFA state has no edges, then it is an accepting state
        if nfa_state.edge1 is None and nfa_state.edge2 is None:
            return True
    
    return False