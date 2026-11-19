#!/usr/bin/env python3
"""Reconstruct an ordinary #758 history from elementary J/L directions."""
from itertools import product
from math import comb

from check_bb33 import HALTING_TARGET, champion_step


def inverse_word(state, word, physical=False):
    """Find all origins, allowing integral signed counters unless physical=True."""
    states = {state}
    for letter in reversed(word):
        origins = set()
        for a, c in states:
            if letter == "J":
                if (a - 2) % 3 == 0:
                    left = (a - 2) // 3
                    right = c + left - 1
                    if left % 2 and (not physical or 0 <= left <= right):
                        origins.add((left, right))
            elif letter == "L":
                if (c - 5) % 6 == 0:
                    q = (c - 5) // 6
                    left = a + 4*q + 3
                    for right in (4*q - 1, 4*q + 1):
                        if not physical or (right >= 0 and left >= 4*q + 3):
                            origins.add((left, right))
            else:
                raise ValueError(letter)
        states = origins
        if not states:
            break
        if len(states) > 1:
            (a, c), (b, d) = sorted(states)
            assert a == b and d == c + 2
    return states


def forward(state):
    a, c = state
    assert c % 2 and a >= 0 and c > 0
    if a % 2 and a <= c:
        return "J", champion_step(a, c)
    if a >= 4*((c+1)//4) + 3:
        return "L", champion_step(a, c)
    return None, None


def mass(state):
    a, c = state
    assert a % 2 and c % 2
    return (a + 2*c - 1)//2


def residue_audit(word, u):
    elementary = word.replace("P", "LL")
    j, p = word.count("J"), word.count("P")
    gained = [0] * (2*p+1)
    seen = 0
    for d in range(3**len(elementary)):
        origins = inverse_word((2*u-4*d-1, 2*d+1), elementary)
        if origins:
            seen += 1
            assert len(origins) == (2 if p else 1)
        for origin in origins:
            t, rem = divmod(u-mass(origin)-2*j-5*p, 2)
            assert rem == 0 and 0 <= t <= 2*p
            gained[t] += 1
    assert seen == (4**p//2 if p else 1)
    assert gained == [comb(2*p, t) for t in range(2*p+1)]


def check_physical():
    # Exhaust all valid origins and all lengths <= 6, including edge guards.
    checked = 0
    for a in range(1, 70, 2):
        for c in range(1, 70, 2):
            state = (a, c)
            word = ""
            for _ in range(6):
                letter, after = forward(state)
                if letter is None:
                    break
                state = after
                word += letter
                origins = inverse_word(state, word, physical=True)
                assert (a, c) in origins
                for origin in origins:
                    reached = origin
                    for expected in word:
                        actual, reached = forward(reached)
                        assert actual == expected
                    assert reached == state
                checked += 1
    return checked


def log_floor_ratio(base_num, base_den, upper_num, upper_den):
    """Largest n >= 0 with (base_num/base_den)^n <= upper_num/upper_den."""
    n = 0
    while upper_den*base_num <= upper_num*base_den:
        n += 1
        upper_den *= base_num
        upper_num *= base_den
    return n


def separation_bounds():
    v = 2*HALTING_TARGET+1
    # c+7 grows at least 3/2 on L; c is initially at least 1.
    bulk_cap = log_floor_ratio(3, 2, v+14, 16)
    # On the six-gap plateau the smaller c+13 evolves by exactly 3/2.
    plateau_cap = log_floor_ratio(3, 1, v+26, 4)
    growth_cap = log_floor_ratio(3, 2, v, 4)
    return bulk_cap, plateau_cap, growth_cap


def sharp_two_bit_bound():
    v = 2*HALTING_TARGET + 1
    # If the first J is in positions 1, 2 or 3, use the initial pure-L gaps.
    for leading, gap in enumerate((36, 48, 72)):
        n = 782-leading
        assert (3*gap-12)*3**n > v*2**n
    # Otherwise the prefix LLL leaves D>=108, and a later J doubles
    # the all-L growth bound. A pure all-L prefix forces c beyond H.
    assert 192*3**780 > v*2**780
    c = 19
    for _ in range(783):
        c = 6*((c+1)//4)+5
    assert c > HALTING_TARGET
    # Two physical states attain a 782-call common future, after a common JJ.
    u = (HALTING_TARGET-10_000)//9*9
    states = [(2*u-4*d-1, 2*d+1) for d in (0, 9)]
    for state in states:
        assert len(inverse_word(state, "JJ", physical=True)) == 1
    for _ in range(782):
        updates = [forward(state) for state in states]
        assert all(letter == "L" for letter, _ in updates)
        states = [state for _, state in updates]
        assert states[0] != states[1]
        assert all(a+2*c <= v for a, c in states)
    assert forward(states[0])[0] != forward(states[1])[0]
    return 783


def sample():
    seed = 3**292+4742
    state = (1, seed)
    for _ in range(292):
        letter, state = forward(state)
        assert letter == "J"
    u = mass(state)
    d = (state[1] - 1)//2
    neighbors = [(2*u-4*x-1, 2*x+1) for x in (d-1, d+1, d+2)]
    first_difference = [None] * len(neighbors)
    word = ""
    points = [state]
    while True:
        letter, after = forward(state)
        if letter is None:
            break
        word += letter
        for k, neighbor in enumerate(neighbors):
            if first_difference[k] is None:
                other, value = forward(neighbor)
                if other != letter:
                    first_difference[k] = len(word)
                else:
                    neighbors[k] = value
        state = after
        points.append(state)
    assert first_difference == [775, None, 779]
    assert neighbors[1] != state
    # At the endpoint reconstruct the entire path with all bulk residues hidden.
    origins = inverse_word(state, word, physical=True)
    assert len(origins) == 2 and points[0] in origins
    assert [x for x in origins if mass(x) == u] == [points[0]]
    return len(word), d, first_difference, [mass(x)-u for x in sorted(origins)]


if __name__ == "__main__":
    audits = 0
    for length in range(5):
        for letters in product("JP", repeat=length):
            for u in (2, 17):
                residue_audit("".join(letters), u)
                audits += 1
    print("coarse residue-slice audits:", audits)
    print("physical prefixes checked:", check_physical())
    print("bulk, plateau, growth caps:", separation_bounds())
    print("sharp lookahead after two known directions ending in J:", sharp_two_bit_bound())
    print("reset witness calls, d, neighbor divergences, origin mass offsets:", sample())
