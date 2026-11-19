#!/usr/bin/env python3
"""Exhaust all possible last resets for four specific #758 terminal states."""
from collections import deque
from check_bb33 import HALTING_TARGET as H, champion_step


FIRST = 1_326_438_094_216_110
# Seed pair, count of map calls from either seed including the halting call,
# total number of states in the inverse search, longest reverse path.
CASES = (
    ((FIRST, FIRST+2), 62, 617, 99),
    ((2_031_355_966_425_479, 2_031_355_966_425_481), 38, 265, 37),
    ((3_335_436_339_933_243, 3_335_436_339_933_245), 34, 213, 36),
    ((H-2, H), 307, 2723, 313),
)


def predecessors(a, c):
    """All incoming edges on the blank-compatible domain for a nonreset state."""
    assert a >= 0 and a != 1 and c >= 1 and c % 2
    parents = set()
    if c % 6 == 5:
        q = (c-5)//6
        for previous_c in (4*q-1, 4*q+1):
            if previous_c >= 1:
                parents.add((a+4*q+3, previous_c))
    if a % 6 == 5:
        previous_a = (a-2)//3
        parents.add((previous_a, c+previous_a-1))
    if a == 3 and c >= 5:
        parents.add((1, c-3))
    if c == 1 and a >= 17 and a % 12 == 5:
        previous_c = (a-8)//3
        parents.add((previous_c+2, previous_c))
    for parent in parents:
        assert champion_step(*parent) == (a, c)
        assert parent[0]+2*parent[1] < a+2*c
    return parents


def terminal(seed, calls):
    state = (1, seed)
    for _ in range(calls-1):
        state = champion_step(*state)
        assert state is not None and state[0] != 1
    assert champion_step(*state) is None
    return state


def exhaust(target, max_nodes):
    queue = deque([(target, 0)])
    seen = {target}
    resets = {}
    longest = 0
    while queue:
        state, depth = queue.popleft()
        longest = max(depth, longest)
        if state[0] == 1:
            resets[state[1]] = depth
            continue
        for parent in predecessors(*state):
            if parent not in seen:
                seen.add(parent)
                if len(seen) > max_nodes:
                    raise RuntimeError("node limit exceeded before exhausting the queue")
                queue.append((parent, depth+1))
    return resets, len(seen), longest


def audit():
    for a in range(100):
        for c in range(1, 100):
            if c % 2 == 0 and a != 1:
                continue
            successor = champion_step(a, c)
            if successor is None or successor[0] == 1:
                continue
            assert (a,c) in predecessors(*successor)

    # A seed strictly below the nearest pair crosses both reset masses in one
    # excursion. The next reset already has larger mass than either candidate.
    state = (1, FIRST-252)
    for _ in range(92):
        state = champion_step(*state)
        assert state is not None and state[0] != 1
    assert champion_step(*state) == (1, FIRST+8)


def main():
    if not __debug__:
        raise SystemExit("run without -O to keep verification enabled")
    audit()
    for (left, right), calls, nodes, depth in CASES:
        target = terminal(left, calls)
        assert terminal(right, calls) == target
        resets, size, longest = exhaust(target, nodes)
        assert resets == {left: calls-1, right: calls-1}
        assert (size, longest) == (nodes, depth)
        label = "H-2, H" if right == H else f"{left}, {right}"
        print(f"{label}: {size} states, maximum depth {longest}, exactly two last resets")


if __name__ == "__main__":
    main()
