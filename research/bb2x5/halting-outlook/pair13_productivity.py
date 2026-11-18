#!/usr/bin/env python3
"""Check a four-cell input/output length potential for line 13."""
from collections import Counter, deque
from pathlib import Path
import json

from pair13 import MACHINE, RULES, cell
from longitudinal import Driver

HERE = Path(__file__).resolve().parent
SEED = ((0, True),) * 4


def composed(start, letter):
    output = letter
    next_state = []
    for s in start:
        s, output = cell(s, output)
        if s is None:
            return None
        next_state.append(s)
    return tuple(next_state), output


def literal(start, letter):
    tape = [s for s, fresh in start]
    flags = [fresh for s, fresh in start]
    head, q = 0, letter
    out = ""
    seen = set()
    while head >= 0:
        key = head, q, tuple(tape), tuple(flags)
        assert key not in seen
        seen.add(key)
        rule = RULES.get((q, tape[head]))
        if rule is None:
            return None
        tape[head], delta, q = rule
        if delta > 0:
            first = flags[head]
            flags[head] = False
            if head == 3:
                out += q
                # Return directly at the cut. A first underlying B is B0 and
                # A on virgin tape returns A. All later completions return A.
                q = q if first else "A"
                continue
        head += delta
    return tuple(zip(tape, flags)), out


def inspect():
    todo = deque([SEED])
    index = {SEED: 0}
    edges = []
    failures = 0
    while todo:
        state = todo.popleft()
        for c in ("A" if state == SEED else "AB"):
            result = composed(state, c)
            assert result == literal(state, c)
            if result is None:
                failures += 1
                continue
            after, word = result
            if after not in index:
                index[after] = len(index)
                todo.append(after)
            edges.append((index[state], index[after], len(word)-1))
    return index, edges, failures


def key(state):
    return " ".join(str(s)+("*" if fresh else "") for s, fresh in state)


def main():
    assert Driver(13).machine == MACHINE
    index, edges, failures = inspect()
    potential = json.loads((HERE/"pair13_potential.json").read_text())
    assert set(potential) == {key(s) for s in index}
    height = [potential[key(s)] for s in index]
    assert height[0] == 0 and all(h <= -1 for h in height[1:])
    assert all(height[i] <= -2 for s, i in index.items() if not s[-1][1])
    assert all(gain <= height[j]-height[i] for i,j,gain in edges)
    print("Four-cell states, completed edges, internal halt edges:", len(index), len(edges), failures)
    print("Potential histogram:", sorted(Counter(height).items()))
    print("All edges agree with physical strip replay. Maximum mature-block potential:",
          max(height[i] for s,i in index.items() if not s[-1][1]))


if __name__ == "__main__":
    main()
