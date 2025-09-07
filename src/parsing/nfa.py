from typing import Optional


class State:
    def __init__(self, label: Optional[str] = None):
        self.label = label # instead of having explictly put the label in each edge, it's more intuitive to look at the labels as the one which contains the character (but you could put the label in the edge)
        # as we know, the Thompson algorithm will construct the ThompsonsNFA with only to possible edges per state
        self.edge1:Optional[State] = None # to what Other state is referencing
        self.edge2:Optional[State] = None# to what Other state is referencing


# the ThompsonsThompsonsNFA class is a class for representing a Non Determistic Finite Automata 
# build with the Thompson algorithm for parsing regex in to nfas.
# The main components of it are the next:
#
# initial: The initial state of the automata (LMAO redundant but still)
# accept: in a Normal NFA we can have many accept's states, but if we follow the Thompsons algorithm, 
# we end up we just one of them

class ThompsonsNFA:
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def postfixToNfa(postfix: str) -> ThompsonsNFA:
    nfaStack:list[ThompsonsNFA] = []

    for c in postfix:
        match c:
            case '∗':

                # We take the ThompsonsNFA that we want to apply the clean
                nfa1 = nfaStack.pop()

                initial:State = State()
                accept:State =  State()

                # from the ThompsonsNFA to the last node
                initial.edge1, initial.edge2 = nfa1.initial, accept #type: ignore

                # and the middle ones, from the end of the actual ThompsonsNFA
                nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

                # and there we know the rest
                nfaStack.append(ThompsonsNFA(initial, accept))

            case'.':

                # We take out the two actual ThompsonsNFA, and put them in a straight edge like Thompson says
                nfa2:ThompsonsNFA = nfaStack.pop()
                nfa1:ThompsonsNFA = nfaStack.pop()

                nfa1.accept.edge1 = nfa2.initial

                # and there we know the rest
                nfaStack.append(ThompsonsNFA(nfa1.initial, nfa2.accept))

            case '|':
                # Same as before
                nfa2:ThompsonsNFA = nfaStack.pop()
                nfa1:ThompsonsNFA =  nfaStack.pop()

                # We create the new one that will point to the ThompsonsNFA
                initial = State()

                # and here we connect with the 'E' to each of those nodes
                initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

                # The last one for the final connection of the ThompsonsNFA 
                accept = State()

                # same here but the nfa are the one connection
                nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

                nfaStack.append(ThompsonsNFA(initial, accept))

            case _:

                if c == '𝜀':
                    c = None # when traversing, it will be better just to check for a 'None' type for taking advantage of the syntatic sugar

                # The ThompsonsNFA as most Data Stuctures we create the references pretty implictly (not the whole thing, but nodes that reference other ones)
                # Soo we create a set for any one consider a character

                # As Pablo told me, we create the symetrical nodes
                initial: State = State() # the initial of the actual ThompsonsNFA we are doing, not the whole construct
                accept: State = State()

                initial.label, initial.edge1 = c, accept #type: ignore

                # Goes to the stack for any other operators
                nfaStack.append(ThompsonsNFA(initial, accept))

    return nfaStack.pop()

