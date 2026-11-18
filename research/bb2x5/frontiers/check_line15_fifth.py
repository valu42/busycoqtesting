#!/usr/bin/env python3
"""Compute the exact first-emission preimage at one and two post-startup cuts."""
from collections import deque
from functools import cache
from itertools import product

from line15 import Left, transfer


@cache
def image(digits, letter):
    word, emitted, _ = transfer(digits, letter)
    return word, emitted


MATURE = transfer(bytes(7), 'AAABB')[0]
ROOT_MATURE = transfer(bytes(7), 'ABBBA')[0]


def dispatch(state, letter):
    """Advance one external entry. A string result decides the fifth letter."""
    parent, child = state
    parent, emitted = image(parent, letter)
    if child is None:
        return emitted[0] if emitted else (parent, None)
    # An empty child word represents the AAAB fringe awaiting its fifth
    # request. Its fifth B both matures it and initializes its own child.
    for request in emitted:
        if not child:
            if request == 'A':
                return 'intermediate A'
            child = MATURE
        else:
            child, output = image(child, request)
            if output:
                return output[0]
    return parent, child


def graph(initial):
    queue = deque([initial])
    path = {initial: ''}
    edges = {}
    shortest = {}
    while queue:
        state = queue.popleft()
        edges[state] = []
        for letter in 'AB':
            after = dispatch(state, letter)
            edges[state].append(after)
            if isinstance(after, str):
                shortest.setdefault(after, path[state]+letter)
            elif after not in path:
                path[after] = path[state]+letter
                queue.append(after)
    return edges, shortest


def lengths(edges, initial):
    """All silent paths terminate; calculate their longest lengths on the DAG."""
    visiting = set()

    @cache
    def longest(state):
        if isinstance(state, str):
            return 0
        if state in visiting:
            raise ValueError('silent cycle')
        visiting.add(state)
        n = 1 + max(longest(child) for child in edges[state])
        visiting.remove(state)
        return n

    return longest(initial)


def first_word(edges, state, incoming):
    for n, letter in enumerate(incoming, 1):
        state = edges[state]['AB'.index(letter)]
        if isinstance(state, str):
            return incoming[:n], state
    raise ValueError('insufficient input prefix')


def verify():
    u = ('BA', 'AAAB')
    z = ('B', 'AAAB', 'AAAAAAB')
    inner = {'AB', 'AAA'} | {w+v for w, v in product(('AAB', 'BBBAA'), z)}
    suffix = {w+v for w, v in product(u, inner)} | {'BBA'+v for v in z}
    expected_bad = {w+'BA'+v for w, v in product(u, suffix)}

    results = {}
    period = Left.period
    for name, initial in [('root', ROOT_MATURE), ('interior', MATURE)]:
        for depth, child in [(1, None), (2, b'')]:
            start = initial, child
            edges, shortest = graph(start)
            n = lengths(edges, start)
            direct = first_word(edges, start, period*16)
            results[name, depth] = len(edges), n, shortest, direct
            if depth == 1:
                bad, good = set(), set()
                stack = [(start, '')]
                while stack:
                    state, w = stack.pop()
                    if state == 'A':
                        bad.add(w)
                    elif state == 'B':
                        good.add(w)
                    else:
                        stack.extend((next_state, w+letter)
                                     for next_state, letter in zip(edges[state], 'AB'))
                if name == 'interior' and (bad != expected_bad or len(good) != 82):
                    raise ValueError('one-strip dangerous prefix language differs')
                phases = {i for i in range(len(period))
                          if first_word(edges, start, (period*4)[i:])[1] == 'A'}
                if phases != ({10} if name == 'root' else {12}):
                    raise ValueError('wrong unanchored period rotations')
    return results


if __name__ == '__main__':
    for (name, depth), (states, limit, shortest, direct) in verify().items():
        print(f"{name}, {depth} cuts: {states} states, at most {limit} requests, "
              f"shortest fifth A {shortest['A']}, shortest fifth B {shortest['B']}")
        if name == 'root':
            print(f"  actual period decides {direct[1]} after {direct[0]}")
