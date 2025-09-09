from typing import Optional
from parsing.nfa import ThompsonsNFA as NFA, State as NFAState
from pprint import pprint

# I wasn't going to write that everytime I want it to type something

# the first key is for state which we want to check there transtitions in question.
# the second is for the label and to which states it goes
TransitionTable = dict[tuple[NFAState,int], dict[str, list[NFAState]]]

EpsilonTable = dict[tuple[NFAState,int], set[tuple[NFAState,int]]]

# the rows in the transition table
StateRow = dict[str, list[NFAState]]

class State:
    def __init__(self, closure:set[tuple[NFAState,int]]):
        self.closure = closure 
        self.edges = {} # for referencing another state, we just check is closure, cause we know they won't repeat

def _addToStateRow(state_row: StateRow, state:Optional[NFAState], label: str) -> None:
    if state is not None:
        state_row[label].append(state)


def _nfaToTransitionTable(nfa: NFA):
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
            _addToStateRow(state_row, state.edge1, label)
            _addToStateRow(state_row, state.edge2, label)

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






def _epsilonClosureTable(transition_table: TransitionTable) -> EpsilonTable:
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
                    pprint(next_state)

                for key in transition_table :

                    # checking if the key is not already, cause of possible self reference
                    if key[0] is next_state and key not in closure : # we check if the state from the "row index" is in the epsilon transitions
                        closure.add(key) # we can re-add it, after all is just a set
                        stack.append(key) # then we added to the stack to see if it has also epislon transitions


        closure_table[state_key] = closure # and after all, we have the closure of our dear stat


    if __debug__:
        print("Epsilon Table")
        pprint(closure_table)

    return closure_table



def nfaToDfa(nfa: NFA):
    transition_table = _nfaToTransitionTable(nfa)

    e_closure = _epsilonClosureTable(transition_table)

    # we could inyect the symbols, but it's just a better idea to get them from the "columns"
    input_symbols = set()

    for row in transition_table.values():

        for sym in row.keys(): # we grabbing all the possible symbols from each row, which we know are the "keys" from the row (like the columns)

            if sym != "𝜀":
                input_symbols.add(sym)

    input_symbols = list(input_symbols) # here are all the posible simbols that are in the regex

    # we get the closure of the first state
    start_closure = set(e_closure[(nfa.initial, 1)])

    # Pretty similar to the nfa, but instead of just having 2 nodes, we have all the collection off them
    dfa_start = State(start_closure) # we won't need the nfa node no more

    # self it's porpuse as a deque, more of it later
    lifo_queue = [dfa_start]

    # and we initialize the closures for creating states
    seen_closures = {str(start_closure): dfa_start}

    while lifo_queue:

        # we go from the first to the last one, like an inverse queue
        current_dfa_state = lifo_queue[0]
        lifo_queue.remove(current_dfa_state)


        for symbol in input_symbols: # we are going to see the transition for each symbol

            next_closure = set()

            for nfa_state in current_dfa_state.closure: # we go through all the states in the closure of the nfa
                
                transitions = transition_table.get(nfa_state, {}) # we start seeing the transitions from the state in the closure

                for target in transitions.get(symbol, []): # and we start looking through the transitions of the actual state on the closure

                    for key in transition_table.keys(): # we go thorugh all the possible states
                        if key[0] is target: # and if we see that state is in the closure
                            next_closure.update(e_closure[key]) # we start agruppating them 

            if next_closure != set():


                # the issue with this approach, is that we can repeate closures,
                # but if we keep track of which ones have we seen, we can skip them
                if str(next_closure) not in seen_closures:
                    new_dfa_state = State(next_closure) # now we create a next state with those edges
                    seen_closures[str(next_closure)] = new_dfa_state # and for not repeating
                    lifo_queue.append(new_dfa_state)

                # and now we have created an edge to that closure, which sooner or later it will also become a State
                current_dfa_state.edges[symbol] = seen_closures[str(next_closure)]


    return dfa_start

