from parsing.nfa import postfixToNfa

# Helper function - Returns set of states that can be reached from state following e arrows
def followes(state):
  # Create a new set, with state as its only member
  states = set()
  states.add(state)

  # Check if state has arrows labelled e from it
  if state.label is None:
    # If there's an 'edge1', follow it
    if state.edge1 is not None or state.edge1 == 'E':
      states |= followes(state.edge1)
    # If there's an 'edge2', follow it
    if state.edge2 is not None or state.edge2 == 'E':
      states |= followes(state.edge2)

  # Returns the set of states
  return states

def matchStringToRegex(postfix, string):
  # Shunt and compile the regular expression
  nfa = postfixToNfa(postfix)

  # The current set of states and the next set of states
  current = set()
  nexts = set()

  # Add the initial state to the current set
  current |= followes(nfa.initial)

  # loop through each character in the string
  for s in string:
    # loop through the current set of states
    for c in current:
      # Check to see if state is labelled 's'
      if c.label == s:
        nexts |= followes(c.edge1)
    # set current to next and clears out next
    current = nexts
    # next is back to an empty set
    nexts = set()

  # Checks if the accept state is in the set for current state
  return (nfa.accept in current)
