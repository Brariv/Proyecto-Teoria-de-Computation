def followes(initial_state):
    # All the states that can be reached and will be visited
    states_to_visit = set()  

    # we push to the stack the initial point of the nfa, and we start pushing to the stack all the subsecuent ones
    stack = [initial_state]  

    while stack:
        state = stack.pop()  

        # If the state is NOT visited, re-add it to the stack
        if state not in states_to_visit:
            states_to_visit.add(state)

            if state.edge1 is not None: # Checking for existance and has a transition different from epsilon
                stack.append(state.edge1)

            if state.edge2 is not None: # Checking for existance and has a transition different from epsilon
                stack.append(state.edge2)

    # Return all reachable states to visit
    return states_to_visit

def matchStringToNfa(nfa, string):
    current = set()  # The current set of states
    nexts = set()    # The next set of states

    # Add the initial state to the current set
    current |= followes(nfa.initial)

    # Loop through each character in the string
    # The main loop will process the tree for each character
    for s in string:
        
        for c in current:

            # Checks state's transition with the current character of the string
            if c.label == s:

                # we put the edge to be checked
                nexts |= followes(c.edge1)

        # Set current to next and starts over
        current = nexts
        nexts = set()  

    # Check if the last state is an accept state
    return nfa.accept in current

