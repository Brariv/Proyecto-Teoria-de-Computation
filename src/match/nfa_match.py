from utils.fa_travel import move
from parsing.nfa import ThompsonsNFA as NFA

def matchStringToNfa(nfa:NFA, string:str) -> bool:

    current = move(nfa.initial) # The current set of states

    # Loop through each character in the string
    # The main loop will process the tree for each character
    for s in string:
        nexts = set() # The next set of states

        for c in current:

            # Checks state's transition with the current character of the string
            if c.label == s and c.edge1 is not None:

                # we put the edge to be checked
                nexts.update(move(c.edge1))

        # Set current to next and starts over
        current = nexts

    # Check if the last state is an accept state
    return nfa.accept in current

