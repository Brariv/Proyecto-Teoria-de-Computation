from collections import deque


def minimize_dfa(dfa_start):
    # Step 1: Collect all DFA states
    queue = deque([dfa_start])
    all_states = set([dfa_start])
    while queue:
        current = queue.popleft()
        for next_state in current.edges.values():
            if next_state not in all_states:
                all_states.add(next_state)
                queue.append(next_state)

    # Step 2: Identify accepting states (those with no outgoing edges in NFA states)
    accepting = set()
    for s in all_states:
        for nfa_state, _ in s.nfa_states:
            if nfa_state.edge1 is None and nfa_state.edge2 is None:
                accepting.add(s)
                break
    non_accepting = all_states - accepting

    partitions = [accepting, non_accepting]

    # Step 3: Partition refinement
    input_symbols = set()
    for state in all_states:
        input_symbols.update(state.edges.keys())

    refined = True
    while refined:
        refined = False
        new_partitions = []
        for group in partitions:
            split_map = {}
            for state in group:
                key = tuple(
                    next((i for i, g in enumerate(partitions) if state.edges.get(sym) in g), None)
                    for sym in input_symbols
                )
                split_map.setdefault(key, set()).add(state)
            if len(split_map) > 1:
                refined = True
                new_partitions.extend(split_map.values())
            else:
                new_partitions.append(group)
        partitions = new_partitions

    # Step 4: Build minimized DFA (representatives for each partition)
    representative = {}
    for group in partitions:
        rep = next(iter(group))
        for state in group:
            representative[state] = rep

    for rep in set(representative.values()):
        new_edges = {}
        for sym, target in rep.edges.items():
            new_edges[sym] = representative[target]
        rep.edges = new_edges

    # Step 5: Return the minimized DFA start
    return representative[dfa_start]
