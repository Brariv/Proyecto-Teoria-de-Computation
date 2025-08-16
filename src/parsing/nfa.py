
# State class - Represents a state with two arrows, labelled by label.
class state:
  # Note that each variable have been
  # set to none to assign no value to each.
  label, edge1, edge2 = None, None, None


# NFA class
class nfa:
  # initial nfa state, single accept state
  initial, accept = None, None

  # NFA constructor
  def __init__(self, initial, accept):
    self.initial, self.accept = initial, accept

def postfixToNfa(pofix):
  # Creates new empty set
  nfaStack = []

  # looping through the postfix expression
  # one character at a time
  for c in pofix:
    # If c is the 'kleene star' operator
    if c == '∗':
      # Pops single NFA from the stack
      nfa1 = nfaStack.pop()
      # Creating new initial and accept state
      initial, accept = state(), state()
      # Join the new initial state to nfa's
      # initial state and new accept state
      initial.edge1, initial.edge2 = nfa1.initial, accept
      # Join old accept state to the new accept state and nfa's initial state
      nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
      # Pushes the new NFA to the stack
      nfaStack.append(nfa(initial, accept))
    # If c is the 'concatenate' operator
    elif c == '.':
      # Popping the stack, NOTE: stacks are L.I.F.O.
      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
      # Merging the accept state of nfa1 to the initial state of nfa2
      nfa1.accept.edge1 = nfa2.initial
      # Appending the new nfa to the stack
      nfaStack.append(nfa(nfa1.initial, nfa2.accept))
    # If c is the 'or' operator
    elif c == '|':
      # Popping the stack
      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
      # creates the initial state
      initial = state()
      initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
      # creates new accept state connecting the accept states
      accept = state()
      # Connects the new Accept state to the two NFA's popped from the stack
      nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
      # Pushes the new NFA to the stack
      nfaStack.append(nfa(initial, accept))
    # If c is the 'plus' operator
    elif c == '+':
      # Pops single NFA from the stack
      nfa1 = nfaStack.pop()
      # Creating new initial and accept state
      accept, initial = state(), state()
      # Join the new initial state to nfa's
      # initial state and new accept state
      initial.edge1 = nfa1.initial
      # Join old accept state to the new accept state and nfa's initial state
      nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
      # Pushes the new NFA to the stack
      nfaStack.append(nfa(initial, accept))
    # if c is the '?' operator
    elif c == '?':
      # Pops a single NFA from the stack
      nfa1 = nfaStack.pop()
      # Creates new initial and accept states for the new NFA
      accept, initial = state(), state()
      # Joins the new accept state to the accept state of nfa1 and the new
      # initial state to the initial state of nfa1
      # Accept connected to inital because empty is acceptable
      initial.edge1, initial.edge2 = nfa1.initial, accept
      # Joins the old accept state to the new accept state
      nfa1.accept.edge1 = accept
      # Pushes the new NFA to the stack
      nfaStack.append(nfa(initial, accept))
    else:
      # accept state, initial state - creating a new instance of the class
      accept, initial = state(), state()
      # joins the initial to a character, edge1 is a pointer which points to the accept state
      initial.label, initial.edge1 = c, accept
      # Appends the new NFA to the stack
      nfaStack.append(nfa(initial, accept))

  # at this point, nfastack should have a single nfa on it
  return nfaStack.pop()



