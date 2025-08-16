
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
                nfa1 = nfaStack.pop()
                initial:State = State()
                accept:State =  State()

                initial.edge1, initial.edge2 = nfa1.initial, accept #type: ignore
                nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept

                nfaStack.append(NFA(initial, accept))

            case'.':
                nfa2:NFA = nfaStack.pop()
                nfa1:NFA = nfaStack.pop()

                nfa1.accept.edge1 = nfa2.initial
                nfaStack.append(NFA(nfa1.initial, nfa2.accept))

            case '|':
                nfa2:NFA = nfaStack.pop()
                nfa1:NFA =  nfaStack.pop()

                initial = State()
                initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial

                accept = State()
                nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept

                nfaStack.append(NFA(initial, accept))

            case _:

                if c == "E":
                    c = None # when traversing, it will be better just to check for a 'None' type for taking advantage of the syntatic sugar

                accept, initial = State(), State()

                initial.label, initial.edge1 = c, accept
                nfaStack.append(NFA(initial, accept))

    return nfaStack.pop()

