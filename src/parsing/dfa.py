from parsing.nfa import NFA, State as NFAState
from pprint import pprint

# I wasn't going to write that everytime I want it to type something

# the first key is for state which we want to check there transtitions in question.
# the second is for the label and to which states it goes
TransitionTable = dict[tuple[NFAState,int], dict[str, list[NFAState]]]

EpsilonTable = dict[tuple[NFAState,int], set[tuple[NFAState,int]]]

# the rows in the transition table
StateRow = dict[str, list[NFAState]]

class State:
    def __init__(self, nfa_states_set):
        self.nfa_states = nfa_states_set
        self.edges = {}



def epsilonClosureTable(transition_table: TransitionTable) -> EpsilonTable:
    closure_table: EpsilonTable = {}

    for state_key in transition_table: # we iterate over all states for checking there closures

        stack: list[tuple[NFAState,int]] = [state_key]

        # The clsoure of the actual state
        closure: set[tuple[NFAState,int]] = {state_key} # have to use the "dict notation", cause how the set "constructor" minimizes the tuple, cause of some F****** reason

        # just for checking the closure of one state
        while stack:
            current = stack.pop()

            current_row = transition_table.get(current, {}) # same thing, if it doesn't have any transitions there's no point in going through it

            # btw, this acts as the base statement, like if it doesn't have any epsilon transition and the stack is empty, we reached the final state
            for next_state in current_row.get("𝜀", []): # get's the epsilon transition, in case they aren't one, it would just ignore it 

                if __debug__:
                    pprint(current)

                # now we start looking through the states on the table
                for key in transition_table:

                    if key[0] is next_state: # we check if the state from the "row index" is in the epsilon transitions
                        closure.add(key) # we can re-add it, after all is just a set
                        stack.append(key) # then we added to the stack to see if it has also epislon transitions


        closure_table[state_key] = closure # and after all, we have the closure of our dear stat


    if __debug__:
        print("Epsilon Table")
        pprint(closure_table)

    return closure_table


def addToStateRow(state_row: StateRow, state:NFAState | None, label: str) -> None:
    if state is not None:
        state_row[label].append(state)


def nfaToTransitionTable(nfa: NFA):
    transition_table:TransitionTable = {}

    stack = [nfa.initial]

    # pretty similar as how we went through the nfa
    visited:set[NFAState] = set()

    state_idx:int = 1 # mosly debugging

    while stack:
        # taking the state
        state:NFAState = stack.pop()

        # we get the labels that are pointing to different neighboars (it should only be 2)
        if state not in visited:
            visited.add(state)

            # we create the temporal row
            state_row: StateRow = {}

            # in the case there's not a label, we know that's an epsilon transition
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

        state_idx+=1 #mostly for debugging, just for keeping track of what state it's having the transitions


    if __debug__: # pretty self explanatory
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
    start_closure = set(e_closure[start_state_key])
    dfa_start = State(start_closure)

    # self it's porpuse as a deque, more of it later
    queue = [dfa_start]

    seen_closures = {str(start_closure): dfa_start}

    while queue:

        # like the left_pop
        current_dfa_state = queue[0]
        queue.remove(current_dfa_state)

        for symbol in input_symbols:
            next_nfa_states = set()

            for nfa_state in current_dfa_state.nfa_states:
                transitions = nfa_table.get(nfa_state, {})
                for target in transitions.get(symbol, []):
                    # Add epsilon closure of target
                    for key in e_closure:
                        if key[0] is target:
                            next_nfa_states.update(e_closure[key])

            if next_nfa_states != set():
                next_closure = set(next_nfa_states)
                if str(next_closure) not in seen_closures:
                    new_dfa_state = State(next_closure)
                    seen_closures[str(next_closure)] = new_dfa_state
                    queue.append(new_dfa_state)

                current_dfa_state.edges[symbol] = seen_closures[str(next_closure)]


    return dfa_start

