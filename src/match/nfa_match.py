
def followes(start_state):
    states = set()
    stack = [start_state]  # stack to avoid recursion

    while stack:
        state = stack.pop()
        if state not in states:
            states.add(state)

            # If state has epsilon transition(s)
            if state.label is None:
                if state.edge1 is not None:
                    stack.append(state.edge1)
                if state.edge2 is not None:
                    stack.append(state.edge2)

    return states


def matchStringToNfa(nfa, string):
    """Simulate NFA on a string without recursion."""

    # Initial ε-closure
    current = followes(nfa.initial)

    # Process input string
    for s in string:
        nexts = set()
        for c in current:
            if c.label == s and c.edge1 is not None:
                nexts.update(followes(c.edge1))
        current = nexts

    # Accept if final state is reachable
    return nfa.accept in current

