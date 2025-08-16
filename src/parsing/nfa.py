from graphviz import Digraph

# Each state will have the label of it, and 2 edges cause of thompson
class State:
    def __init__(self, label=None):
        self.label = label
        self.edge1 = None
        self.edge2 = None


# cause of how those thompson work, there will be just one acceptation state
class NFA:
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

# Function to create the NFA from postfix notation
def postfixToNfa(postfix: str) -> Digraph:
    nfaStack = []

    # Graphviz Dot object
    dot:Digraph = Digraph()
    visited:set = set()

    # Uses closures to get the visted ones
    def add_state(state, state_id):
        if state not in visited:
            visited.add(state)
            dot.node(state_id, label=str()) # puttin the emtpy string for it to not have a label 
            
            if state.edge1:
                dot.edge(state_id, str(id(state.edge1)), label=state.label if state.label else "E") # the one and only, friendly utf-8 epsilon
            if state.edge2:
                dot.edge(state_id, str(id(state.edge2)), label="E") # the one and only, friendly utf-8 epsilon

    # Processing each symbol in the postfix expression
    for c in postfix:
        if c == '∗':
            nfa1 = nfaStack.pop()
            initial, accept = State(), State()

            initial.edge1, initial.edge2 = nfa1.initial, accept
            nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

            nfaStack.append(NFA(initial, accept))

        elif c == '.':
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            nfa1.accept.edge1 = nfa2.initial
            nfaStack.append(NFA(nfa1.initial, nfa2.accept))

        elif c == '|':
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            initial = State()
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

            accept = State()
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

            nfaStack.append(NFA(initial, accept))

        else:
            if c == "E":
                c = None
            accept, initial = State(), State()
            initial.label, initial.edge1 = c, accept
            nfaStack.append(NFA(initial, accept))

    final_nfa = nfaStack.pop()

    # need to create the afn initial point stack in here, cause the id function needs the closure
    stack = [(final_nfa.initial, str(id(final_nfa.initial)))]

    while stack:
        state, state_id = stack.pop()
        add_state(state, state_id)

        if state.edge1 and state.edge1 not in visited:
            stack.append((state.edge1, str(id(state.edge1))))
        if state.edge2 and state.edge2 not in visited:
            stack.append((state.edge2, str(id(state.edge2))))

    dot.render('nfa_output', format='png', cleanup=True)  # Save the graph as a PNG image

    return final_nfa
