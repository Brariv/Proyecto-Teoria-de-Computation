from parsing.dfa import State as DFA

def minimizeDfa(dfa_start: DFA) -> DFA:
    # Step 1: Collect all DFA states
    all_states = set() # Empty set for collecting all the states
    stack = [dfa_start] # we use a stack for doing a DFS
    while stack:
        state = stack.pop() # we take the last state
        if state not in all_states: # if we haven't seen it
            all_states.add(state)
            for target in state.edges.values(): # we go through all the edges
                stack.append(target) # and we add them to the stack for checking them later

    # Step 2: Identify accepting states (those with no outgoing edges in NFA states)
    accepting = set() # set for the accepting states
    for s in all_states:
        for nfa_state, _ in s.closure:
            if nfa_state.edge1 is None and nfa_state.edge2 is None:
                accepting.add(s) # if the nfa inside of the state of the dfa has no edges, then the dfa state is accepting
                break
    non_accepting = all_states - accepting # the rest are non accepting

    partitions = [accepting, non_accepting] #we set the initial partitions

    # Step 3: Partition refinement
    input_symbols = set() # we get all the input symbols
    for s in all_states:
        input_symbols.update(s.edges.keys()) # we go through all the edges of each state and we add the symbols to the set

    refined = True # we use this for checking if we have refined the partitions
    while refined:
        new_partitions = [] # new partitions for this iteration
        for group in partitions: # we go through each partition of the partitions
            split_map = {} # we use this for splitting the groups
            for state in group:
                key = tuple(
                    # in case that the partition doesn't return anything it will just put a None value
                    next((i for i, g in enumerate(partitions) if state.edges.get(sym) in g), None)
                    for sym in input_symbols
                )
                split_map.setdefault(key, set()).add(state) # we add the state to the split map
            if len(split_map) > 1: # if we splitted the group we add it to the new partitions
                refined = True
                new_partitions.extend(split_map.values())
            else: # if the last split map is only one, we add the group as it is and we are done
                refined = False
                new_partitions.append(group)
        partitions = new_partitions

    # Step 4: Build minimized DFA (representatives for each partition)
    representative = {} #for the new DFA minimized
    for group in partitions: #iterate trogh partition
        if not group: # if not any more partitions
            continue
        rep = next(iter(group)) # to check the next partition 
        for state in group:
            representative[state] = rep # the next state is the next partition

    for rep in set(representative.values()): #define the edges for the new states
        new_edges = {} 
        for sym, target in rep.edges.items(): # grab past simbol of the edge and adds it to representative
            new_edges[sym] = representative[target]
        rep.edges = new_edges # the rest of the edges is added at last

    # Step 5: Return the minimized DFA start
    return representative[dfa_start]
