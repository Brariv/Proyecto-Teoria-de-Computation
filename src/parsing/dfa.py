from parsing.nfa import NFA, State
from pprint import pprint

def addToStateRow(state_row: list[tuple[str,State]], state:State | None, label: str | None) -> None:
    if (state is not None):
        if (label is not None):
            state_row.append((label, state))
        else:
            state_row.append(("𝜀", state))


def nfaToTransitionTable(nfa: NFA):
    # the first key is for state which we want to check there transtitions in question.
    # the second is for the label and to which states it goes
    transition_table:dict[tuple[State,int],list[tuple[str,State]]] = {}

    stack = [nfa.initial]

    visited:set[State] = set()

    state_idx:int = 1

    while stack:
        # taking the state
        state:State = stack.pop()

        # we save the reference to the neighboars in to the transition_table

        # We get the labels that are pointing to different neighboars (it should only be 2)
        if state not in visited:
            visited.add(state)
            # We create the temporal row
            state_row: list[tuple[str, State]] = list()

            # add the state to the rows for each label
            addToStateRow(state_row, state.edge1, state.label)
            addToStateRow(state_row, state.edge2, state.label)

            # and off you go to the transition table
            transition_table[(state,state_idx)] = state_row # I f**** hate type inference in dynamic programming languages

        # We don't want it to add them if we already pass through them
        if state.edge1 and state.edge1 not in visited:
            stack.append(state.edge1)
        if state.edge2 and state.edge2 not in visited:
            stack.append(state.edge2)

        state_idx+=1

    if __debug__:
        pprint(transition_table)

    return transition_table



#def minimizeTransitionTable(transition_table:dict[tuple[State,int],list[tuple[str,State]]]):
#    for state in transition_table.items():

