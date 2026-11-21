"""Finite, exact invariant checking for the Wily Coyote sweep.

A successful result proves the three inductive-language obligations by exhaustive
reachability of finite product automata, for words of every finite length.
A failure gives the shortest witness in shortlex order. No external dependencies.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from certificates import STEP, END, sweep, pass_word

@dataclass(frozen=True)
class DFA:
    transitions: tuple[tuple[int, int], ...]
    accepting: frozenset[int]
    initial: int = 0

    def __post_init__(self):
        n = len(self.transitions)
        assert 0 <= self.initial < n
        assert all(0 <= q < n for row in self.transitions for q in row)
        assert all(0 <= q < n for q in self.accepting)

    def step_word(self, q: int, word: str) -> int:
        for b in word:
            q = self.transitions[q][int(b)]
        return q

    def accepts(self, word: str) -> bool:
        return self.step_word(self.initial, word) in self.accepting

BAD = DFA(((1, 2), (3, 0), (2, 1), (3, 3)), frozenset({1}))
SAFE = DFA(BAD.transitions, frozenset({0, 2, 3}))
ENDS_00 = DFA(((1, 0), (2, 0), (2, 0)), frozenset({2}))

def shortest_product_witness(initial, successors, failure):
    seen = {initial: (None, '')}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        if failure(state):
            chars = []
            here = state
            while seen[here][0] is not None:
                here, char = seen[here]
                chars.append(char)
            return ''.join(reversed(chars)), len(seen)
        for bit, nxt in enumerate(successors(state)):
            if nxt not in seen:
                seen[nxt] = (state, str(bit))
                queue.append(nxt)
    return None, len(seen)

def verify_invariant(candidate: DFA, prepend: bool = True, seed: str | None = None) -> dict:
    if seed is None:
        seed = '00' if prepend else '001100'
    def safety_step(state):
        p, b = state
        return [(candidate.transitions[p][i], BAD.transitions[b][i]) for i in (0, 1)]

    unsafe, safety_states = shortest_product_witness(
        (candidate.initial, BAD.initial), safety_step,
        lambda state: state[0] in candidate.accepting and state[1] in BAD.accepting)

    def closure_step(state):
        inp, out, mode = state
        result = []
        for bit in (0, 1):
            emitted, nxt_mode = STEP[mode][bit]
            result.append((candidate.transitions[inp][bit],
                           candidate.transitions[out][emitted], nxt_mode))
        return result

    def closure_failure(state):
        inp, out, mode = state
        end = END[mode]
        return (inp in candidate.accepting and end is not None and
                candidate.step_word(out, end) not in candidate.accepting)

    failed_closure, closure_states = shortest_product_witness(
        (candidate.initial, candidate.step_word(candidate.initial, '0' if prepend else ''), 0),
        closure_step, closure_failure)
    contains_start = candidate.accepts(seed)
    return {'contains_start': contains_start,
            'unsafe_word': unsafe,
            'closure_counterexample': failed_closure,
            'closure_image': None if failed_closure is None else
                (sweep(failed_closure) if prepend else pass_word(failed_closure)),
            'safety_product_states': safety_states,
            'closure_product_states': closure_states,
            'valid': contains_start and unsafe is None and failed_closure is None}

def reduced_invariant_dfa(original: DFA) -> DFA:
    """DFA for {x != empty: exists k>=1, (01)^k 00 x in original}.

    If original is a valid F-invariant, Theorem 8 proves this DFA is a
    valid P0-invariant containing 001100. This transformation does not
    assume validity and can be used on any input DFA.
    """
    prefix_states = set()
    seen = set()
    q = original.step_word(original.initial, '01')
    while q not in seen:
        seen.add(q)
        prefix_states.add(original.step_word(q, '00'))
        q = original.step_word(q, '01')
    start = (frozenset(prefix_states), False)
    states = [start]
    ids = {start: 0}
    transitions = []
    accepting = set()
    for index, (subset, nonempty) in enumerate(states):
        if nonempty and subset & original.accepting:
            accepting.add(index)
        row = []
        for bit in (0, 1):
            nxt = (frozenset(original.transitions[p][bit] for p in subset), True)
            if nxt not in ids:
                ids[nxt] = len(states)
                states.append(nxt)
            row.append(ids[nxt])
        transitions.append(tuple(row))
    return DFA(tuple(transitions), frozenset(accepting))

if __name__ == '__main__':
    import json
    for name, dfa in [('next_sweep_safe', SAFE), ('ends_00', ENDS_00)]:
        print(name, json.dumps(verify_invariant(dfa), sort_keys=True))
