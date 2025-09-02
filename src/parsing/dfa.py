from collections import deque
from parsing.nfa import NFA, State
from pprint import pprint


class DFAState:
    def __init__(self, nfa_states_set):
        self.nfa_states = nfa_states_set
        self.edges = {}



def epsilonClosureTable(transition_table: dict[tuple[State,int], dict[str, list[State]]]) -> dict[tuple[State,int], set[tuple[State,int]]]:
    closure_table: dict[tuple[State,int], set[tuple[State,int]]] = {}

    for s_key in transition_table:
        stack: list[tuple[State,int]] = [s_key]
        closure: set[tuple[State,int]] = {s_key}

        while stack:
            current = stack.pop()
            row = transition_table.get(current, {})
            for next_state in row.get("𝜀", []):
                # find tuple key(s) in table corresponding to this State object
                for key in transition_table:
                    if key[0] is next_state and key not in closure:
                        closure.add(key)
                        stack.append(key)
        closure_table[s_key] = closure


    if __debug__:
        print("Epsilon Table")
        pprint(closure_table)

    return closure_table


def addToStateRow(state_row: dict[str,list[State]], state:State | None, label: str) -> None:
    if state is not None:
        state_row[label].append(state)


def nfaToTransitionTable(nfa: NFA):
    # the first key is for state which we want to check there transtitions in question.
    # the second is for the label and to which states it goes
    transition_table:dict[tuple[State,int],dict[str, list[State]]] = {}

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
            state_row: dict[str, list[State]] = dict()


            label:str
            if state.label is not None:
                label = state.label
            else: 
                label = "𝜀"

            state_row[label] = []

            # add the state to the rows for each label
            addToStateRow(state_row, state.edge1, label)
            addToStateRow(state_row, state.edge2, label)

            # and off you go to the transition table
            transition_table[(state,state_idx)] = state_row # I f**** hate type inference in dynamic programming languages

        # We don't want it to add them if we already pass through them
        if state.edge1 and state.edge1 not in visited:
            stack.append(state.edge1)
        if state.edge2 and state.edge2 not in visited:
            stack.append(state.edge2)

        state_idx+=1

    if __debug__:
        print("Transition Table")
        pprint(transition_table)

    return transition_table




def nfaToDfa(nfa: NFA):
    # Step 1: Build the NFA transition table
    nfa_table = nfaToTransitionTable(nfa)
    
    # Step 2: Compute epsilon closures
    e_closure = epsilonClosureTable(nfa_table)
    
    # Step 3: Extract input symbols (excluding epsilon)
    input_symbols = set()
    for row in nfa_table.values():
        for sym in row:
            if sym != "𝜀":
                input_symbols.add(sym)
    input_symbols = list(input_symbols)

    # Step 4: Initialize DFA
    start_state_key = (nfa.initial, 1)
    start_closure = frozenset(e_closure[start_state_key])
    dfa_start = DFAState(start_closure)

    queue = deque([dfa_start])
    seen_closures = {start_closure: dfa_start}

    while queue:
        current_dfa_state = queue.popleft()
        for symbol in input_symbols:
            next_nfa_states = set()
            for nfa_state in current_dfa_state.nfa_states:
                transitions = nfa_table.get(nfa_state, {})
                for target in transitions.get(symbol, []):
                    # Add epsilon closure of target
                    for key in e_closure:
                        if key[0] is target:
                            next_nfa_states.update(e_closure[key])
            if next_nfa_states:
                next_closure = frozenset(next_nfa_states)
                if next_closure not in seen_closures:
                    new_dfa_state = DFAState(next_closure)
                    seen_closures[next_closure] = new_dfa_state
                    queue.append(new_dfa_state)
                # Create DFA edge
                current_dfa_state.edges[symbol] = seen_closures[next_closure]

    # Optional: return both start state and all DFA states

    return dfa_start

