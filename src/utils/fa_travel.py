from parsing.nfa import  State


def move(start_state:State) -> set[State]:
    # All the states that can be reached and will be visited
    states_to_visit:set[State] = set()

    # we push to the stack the initial point of the nfa, and we start pushing to the stack all the subsecuent ones
    stack = [start_state]

    while stack:
        state = stack.pop()

        # If the state is NOT visited, re-add it to the stack
        if state not in states_to_visit:
            states_to_visit.add(state)

            
            if state.label is None: # Checking for existance and has a transition

                if state.edge1 is not None: # Checking for children nodes
                    stack.append(state.edge1)
                if state.edge2 is not None: # Checking for children nodes
                    stack.append(state.edge2)

    # Return all reachable states to visit
    return states_to_visit



