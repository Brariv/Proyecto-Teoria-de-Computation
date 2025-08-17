
from drawing import nfa


class State:
    def __init__(self, label: str|None =None):
        self.label = label # instead of having explictly put the label in each edge, it's more intuitive to look at the labels as the one which contains the character (but you could put the label in the edge)
        # as we know, the Thompson algorithm will construct the NFA with only to possible edges per state
        self.edge1 = None # to what Other state is referencing
        self.edge2 = None# to what Other state is referencing



class NFA:
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def postfixToNfa(postfix: str) -> NFA:
    nfaStack:list[NFA]| list[None] = []

    for c in postfix:
        match c:
            case '∗':

                # We take the NFA that we want to apply the clean
                nfa1 = nfaStack.pop()

                initial:State = State()
                accept:State =  State()

                # from the NFA to the last node
                initial.edge1, initial.edge2 = nfa1.initial, accept #type: ignore

                # and the middle ones, from the end of the actual NFA
                nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

                # and there we know the rest
                nfaStack.append(NFA(initial, accept))

            case'.':

                # We take out the two actual NFA, and put them in a straight edge like Thompson says
                nfa2:NFA = nfaStack.pop()
                nfa1:NFA = nfaStack.pop()

                nfa1.accept.edge1 = nfa2.initial

                # and there we know the rest
                nfaStack.append(NFA(nfa1.initial, nfa2.accept))

            case '|':
                # Same as before
                nfa2:NFA = nfaStack.pop()
                nfa1:NFA =  nfaStack.pop()

                # We create the new one that will point to the NFA
                initial = State()

                # and here we connect with the 'E' to each of those nodes
                initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

                # The last one for the final connection of the NFA 
                accept = State()

                # same here but the nfa are the one connection
                nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

                nfaStack.append(NFA(initial, accept))

            case _:

                if c == '𝜀':
                    c = None # when traversing, it will be better just to check for a 'None' type for taking advantage of the syntatic sugar

                # The NFA as most Data Stuctures we create the references pretty implictly (not the whole thing, but nodes that reference other ones)
                # Soo we create a set for any one consider a character

                # As Pablo told me, we create the symetrical nodes
                initial: State = State() # the initial of the actual NFA we are doing, not the whole construct
                accept: State = State()

                initial.label, initial.edge1 = c, accept #type: ignore

                # Goes to the stack for any other operators
                nfaStack.append(NFA(initial, accept))

    return nfaStack.pop()

