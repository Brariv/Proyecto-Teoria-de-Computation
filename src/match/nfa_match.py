
# Helper function - Returns set of states that can be reached from state following e arrows
def followes(state):
    states = set()  # A set to store the reachable states
    stack = [state]  # A stack to keep track of states to process
    
    while stack:
        current_state = stack.pop()  # Pop the last state from the stack
        
        # If the state is not already visited, process it
        if current_state not in states:
            states.add(current_state)

            # If there is an 'edge1' and it's not None, push it onto the stack
            if current_state.edge1 is not None:
                stack.append(current_state.edge1)
            
            # If there is an 'edge2' and it's not None, push it onto the stack
            if current_state.edge2 is not None:
                stack.append(current_state.edge2)

    return states

def matchStringToNfa(nfa, string):
    current = set()  # The current set of states
    nexts = set()    # The next set of states

    # Add the initial state to the current set
    current |= followes(nfa.initial)

    # Loop through each character in the string
    for s in string:
        
        # Loop through the current set of states
        for c in current:
            
            # Check if state is labeled with the current character 's'
            if c.label == s:
                
                # Add reachable states to nexts
                nexts |= followes(c.edge1)

        # Set current to next and clears out next
        current = nexts
        nexts = set()  # Reset nexts for the next iteration

    # Check if the accept state is in the set of current states
    return nfa.accept in current

