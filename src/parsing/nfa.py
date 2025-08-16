
# State class - Represents a state with two arrows, labelled by label.


# Dunno how own class-type in class
class State:
    label = None,
    edge1 = None,
    edge2 = None


# NFA class
class Nfa:
    initial, accept = None, None
    
    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept

def postfixToNfa(pofix):
  # Creates new empty set
  nfaStack = []

  for c in pofix:
    if c == '∗':
        nfa1 = nfaStack.pop()

        initial, accept = State(), State()

        initial.edge1, initial.edge2 = nfa1.initial, accept #type: ignore

        nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

        nfaStack.append(Nfa(initial, accept))
    elif c == '.':
      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()

      nfa1.accept.edge1 = nfa2.initial

      nfaStack.append(Nfa(nfa1.initial, nfa2.accept))
    elif c == '|':

      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()

      initial = State()
      initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

      accept = State()
      nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

      nfaStack.append(Nfa(initial, accept))

    else:

      accept, initial = State(), State()

      initial.label, initial.edge1 = c, accept  #type: ignore

      nfaStack.append(Nfa(initial, accept))

  # at this point, nfastack should have a single nfa on it
  return nfaStack.pop()



