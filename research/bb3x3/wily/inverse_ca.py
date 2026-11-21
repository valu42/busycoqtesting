#!/usr/bin/env python3
"""Independent exact checks for the clipped linear-CA description of Wily a.

The all-length statements and their proofs are in INVERSE_CA.md.  This program
checks the transducer implementation, finite boundary formulas, and finite
automaton certificates.  It does not decide the blank orbit.

Polynomials over F_2 are integers whose i-th bit is the coefficient of z^i.
Words are written least-significant coefficient first, matching the scan order.
"""
from collections import deque
from itertools import product

from padding import FINITE, VIRTUAL, scan, virtual_step

P = 0b111       # 1 + z + z^2
D = 0b110       # z + z^2 = P + 1
TAIL_DEN = 0b101  # 1 + z^2; t = 1/(1+z^2)


def polynomial(word):
    return sum(int(bit) << i for i, bit in enumerate(word))


def word(poly, width):
    return "".join(str((poly >> i) & 1) for i in range(width))


def multiply(left, right):
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def remainder(poly, divisor):
    while poly.bit_length() >= divisor.bit_length():
        poly ^= divisor << (poly.bit_length() - divisor.bit_length())
    return poly


def completed_numerator(bits):
    """Numerator of bits*t over the common denominator 1+z^2."""
    return multiply(TAIL_DEN, polynomial(bits)) ^ (1 << len(bits))


def inverse_ca(bits):
    """First len(bits) coefficients of a^{-1}(bits...), using the clipped CA."""
    first = bits.find("11")
    cutoff = len(bits) if first < 0 else first + 1
    q = polynomial(bits[:cutoff])
    return word(polynomial(bits) ^ 1 ^ multiply(D, q), len(bits))


def double_fibonacci_certificate():
    """All infinite Y for which Y and P*Y+1 have no adjacent ones.

    A state is (previous_previous_Y, previous_Y, previous_X).  The fictitious
    initial Y memory is 10, and previous_X=0 imposes no restriction at bit zero.
    Remove states with no infinite continuation.  The resulting exact graph
    has precisely the two labelled rays 0^omega and (10)^omega.
    """
    initial = (1, 0, 0)
    pending = deque([initial])
    states = {initial}
    transitions = {}
    while pending:
        state = pending.popleft()
        transitions[state] = []
        for y in (0, 1):
            x = y ^ state[0] ^ state[1]
            if state[1] and y or state[2] and x:
                continue
            target = (state[1], y, x)
            transitions[state].append((y, target))
            if target not in states:
                states.add(target)
                pending.append(target)
    productive = set(states)
    while True:
        following = {
            state for state in productive
            if any(target in productive for _, target in transitions[state])
        }
        if following == productive:
            break
        productive = following
    graph = {
        state: [(bit, target) for bit, target in transitions[state]
                if target in productive]
        for state in productive
    }
    expected = {
        (1, 0, 0): [(0, (0, 0, 1)), (1, (0, 1, 0))],
        (0, 0, 1): [(0, (0, 0, 0))],
        (0, 0, 0): [(0, (0, 0, 0))],
        (0, 1, 0): [(0, (1, 0, 1))],
        (1, 0, 1): [(1, (0, 1, 0))],
    }
    assert graph == expected
    return graph


def cycle_lengths(permutation):
    visited = set()
    lengths = []
    for start in range(len(permutation)):
        if start in visited:
            continue
        current, size = start, 0
        while current not in visited:
            visited.add(current)
            size += 1
            current = permutation[current]
        assert current == start
        lengths.append(size)
    return sorted(lengths)


def verify():
    checked = repairs = 0
    for width in range(15):
        for chars in product("01", repeat=width):
            bits = "".join(chars)
            emitted, mode = scan(bits)
            assert inverse_ca(emitted) == bits
            checked += 1
            u, v = polynomial(bits), polynomial(emitted)
            if mode < 4:
                # Before entering copy, the active modes encode output memory
                # a=10, b=01, c=00, d=11.  These are the omitted high CA cells.
                boundary = (
                    1 << width,
                    (1 << width) ^ (1 << (width + 1)),
                    0,
                    1 << (width + 1),
                )[mode]
                assert multiply(P, v) == u ^ 1 ^ boundary
            else:
                first = emitted.index("11")
                q = polynomial(emitted[:first + 1])
                assert u == v ^ 1 ^ multiply(D, q)
            if mode == 0:
                repairs += 1
                actual = emitted + FINITE[mode]
                virtual = emitted + VIRTUAL[mode]
                wr = completed_numerator(actual)
                wv = completed_numerator(virtual)
                wu = completed_numerator(bits)
                # Inverse of a repair is exactly one flipped completion bit.
                assert (multiply(P, wr) ^ TAIL_DEN) == (
                    wu ^ (TAIL_DEN << (width + 1))
                )
                # The output repair defect has exactly two P factors.
                assert wr ^ wv == (multiply(0b11, multiply(P, P)) << (width + 1))
    graph = double_fibonacci_certificate()
    a_permutation = [polynomial(scan(word(i, 3))[0]) for i in range(8)]
    t_permutation = [(multiply(P, i) ^ 1) & 7 for i in range(8)]
    assert cycle_lengths(a_permutation) == [8]
    assert cycle_lengths(t_permutation) == [4, 4]
    # Repairs are invisible mod P^2, but this quotient is not a dynamical one.
    first, second = "0", "001100"
    delta = completed_numerator(first) ^ completed_numerator(second)
    assert delta == multiply(D, multiply(P, P))
    image_first, _ = virtual_step(first)
    image_second, _ = virtual_step(second)
    assert image_first == "" and image_second == "110100"
    image_delta = completed_numerator(image_first) ^ completed_numerator(image_second)
    assert image_delta == 0b1100110 and remainder(image_delta, P) != 0
    print("Clipped inverse and boundary formulas checked on", checked, "words.")
    print("Exact single-bit / P^2 repair identities checked at", repairs, "repairs.")
    print("Double-Fibonacci invariant graph verified:", len(graph), "productive states.")
    print("Depth-three cycle obstruction verified: a=[8], unclipped CA=[4,4].")
    print("One-sweep failure of the P^2 congruence quotient verified.")
    print("These theorems do not decide the blank orbit.")


if __name__ == "__main__":
    verify()
