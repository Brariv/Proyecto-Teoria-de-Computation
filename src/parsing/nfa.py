from graphviz import Digraph
# State class - Represents a state with two arrows, labelled by label.
class state:
    label, edge1, edge2 = None, None, None


# NFA class
class nfa:
    initial, accept = None, None
    
    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept

def postfixToNfa(pofix):
      # Creates new empty set
    nfaStack:list = []


    for c in pofix:
        if c == '∗':
            nfa1 = nfaStack.pop()

            initial, accept = state(), state()

            initial.edge1, initial.edge2 = nfa1.initial, accept #type: ignore

            nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

            nfaStack.append(nfa(initial, accept))
        elif c == '.':
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()

            nfa1.accept.edge1 = nfa2.initial

            nfaStack.append(nfa(nfa1.initial, nfa2.accept))
        elif c == '|':

            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()

            initial = state()
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

            accept = state()
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

            nfaStack.append(nfa(initial, accept))

        else:

            # the empty string, the one and only "UTF-8 friendly Epsilon"
            if c == "E":
                c = None

            accept, initial = state(), state()

            initial.label, initial.edge1 = c, accept #type: ignore

            nfaStack.append(nfa(initial, accept))

  # at this point, nfastack should have a single nfa on it
    return nfaStack.pop()



