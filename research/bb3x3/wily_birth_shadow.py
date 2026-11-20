#!/usr/bin/env python3
"""Check the Wily exterior decoder against the machine's original carry table."""
from itertools import product

from check_bb33 import WILY

# False means token boundary, True means the second bit of a B is due.
E = ((), False)
L = ((), True)
M = ((0,), True)
S = ((1,), False)
J = ((3, 1), False)
# Each entry is (next state, completed token). None means rejection.
TABLE = {
    E: ((L, ""), (S, "A")),
    L: (None, (E, "B")),
    M: ((S, "B"), None),
    S: ((J, "A"), (M, "")),
    J: ((M, ""), (J, "A")),
}


def through(word, mode, inverse=False):
    out = []
    for bit in word:
        if mode >= 0:
            row = WILY.rules[mode]
            if inverse:
                old = 0 if row[0][0] == bit else 1
                mode = row[old][1]
                bit = old
            else:
                bit, mode = row[bit]
        out.append(bit)
    return tuple(out)


def pullback(mode, exterior):
    """Old virtual exterior needed to write the physical allocation."""
    return through(WILY.extension[mode] + exterior, mode, inverse=True)


def encode(tokens, last=()):
    word = last
    for token in reversed(tokens):
        if token == "A":
            word = (1,) + through(word, 1, inverse=True)
        else:
            assert token == "B"
            word = (0, 1) + word
    return word


def derived_step(state, bit):
    pending, halfway = state
    following = []
    for mode in pending:
        bit, carry = WILY.rules[mode][bit]
        if carry >= 0:
            following.append(carry)
    if halfway:
        return ((tuple(following), False), "B") if bit else None
    if bit:
        return (tuple(following + [1]), False), "A"
    return (tuple(following), True), ""


def decode(bits, state=E):
    tokens = []
    for bit in bits:
        step = TABLE[state][bit]
        if step is None:
            return None, "".join(tokens)
        state, token = step
        tokens.append(token)
    return state, "".join(tokens)


def check_coding():
    for state, entries in TABLE.items():
        assert tuple(derived_step(state, bit) for bit in (0, 1)) == entries

    for length in range(10):
        for tail in product((0, 1), repeat=length):
            assert pullback(0, tail) == (1,) + through(tail, 2, inverse=True)
            assert pullback(3, tail) == (1, 0) + tail
            assert pullback(2, tail) == pullback(3, pullback(3, tail))
            for mode, tokens in ((0, "A"), (3, "B"), (2, "BB")):
                assert pullback(mode, (1,) + tail) == (1,) + encode(tokens, tail)

    for length in range(13):
        for tokens in product("AB", repeat=length):
            word = encode(tokens)
            state, actual = decode(word)
            assert state is not None and not state[1] and actual == "".join(tokens)

    # All accepted finite words ending at token boundaries are exactly
    # the encoded token words; the remaining viable words are halfway into B.
    for length in range(15):
        for word in product((0, 1), repeat=length):
            state, tokens = decode(word)
            if state is None:
                continue
            if state[1]:
                assert encode(tokens + "B")[:length] == word
            else:
                assert encode(tokens) == word


def integer_bits(value, width):
    return tuple((value >> i) & 1 for i in range(width))


def periodic_outcomes(period):
    outcomes = set()
    for start in TABLE:
        state, phase = start, 0
        seen, tokens = {}, []
        while (state, phase) not in seen:
            seen[state, phase] = len(tokens)
            step = TABLE[state][period[phase]]
            if step is None:
                break
            state, token = step
            tokens.append(token)
            phase = (phase + 1) % len(period)
        else:
            outcomes.add("".join(tokens[seen[state, phase]:]))
    return outcomes


def check_periodic():
    assert periodic_outcomes((1,)) == {"A"}
    assert periodic_outcomes((0,)) == {"AB", "BA"}
    for period in ((0, 1), (1, 0)):
        assert periodic_outcomes(period) == {"B"}
    for width in range(1, 90):
        for mode, later, earlier in ((0, -5, -5), (0, 29, 7), (3, 7, 29)):
            encoded = pullback(mode, integer_bits(later, width))
            assert encoded == integer_bits(earlier, len(encoded))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("run with assertions enabled")
    check_coding()
    check_periodic()
    print("Five-state decoder, allocation pullbacks and three tail classifications verified.")
