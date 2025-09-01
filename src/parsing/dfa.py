from typing import Dict
from parsing.nfa import NFA, State
from utils.fa_travel import move




def nfaToTransitionTable(nfa: NFA):
    # the first key is for state which we want to check there transtitions in question.
    # the second is for the label and to which states it goes
    transition_table:dict[State,dict[str,State]] = {}

    stack = [nfa.initial]

    visited:set[State] = set()

    while stack:
        # taking the state
        state:State = stack.pop()

        # we save the reference to the neighboars in to the transition_table

        # We get the labels that are pointing to different neighboars (it should only be 2)
        if state not in visited:
            visited.add(state)
            # We create the temporal row
            state_row: dict[str,State] = dict()

            # we add the edges
            if (state.edge1 is not None):
                if (state.edge1.label is not None):
                    label_1: str = state.edge1.label
                    state_row[label_1] = state.edge1
                else:
                    label_1: str = "𝜀" 
                    state_row[label_1] = state.edge1


            if (state.edge2 is not None):
                if (state.edge2.label is not None):
                    label_2: str = state.edge2.label
                    state_row[label_2] = state.edge2
                else:
                    label_2: str = "𝜀"
                    state_row[label_2] = state.edge2



            # and off you go to the transition table
            transition_table[state] = state_row # I f**** hate type inference in dynamic programming languages

        # We don't want it to add them if we already pass through them
        if state.edge1 and state.edge1 not in visited:
            stack.append(state.edge1)
        if state.edge2 and state.edge2 not in visited:
            stack.append(state.edge2)

    print(transition_table)
        




