"""Verify the complete binary residue graphs for the two cusp halters and H_m."""

from fractions import Fraction
from math import gcd

from check_758_lifts import D as H_DEN, OFFSET as H_OFFSET
from cusp_terminals_758 import BASE_I, D as CUSP_DEN, Q as CUSP_Q


SIZE = 32768
PAIR_U = (5, 9, 7, 7)
PAIR_D = (20, 35, 26, 29)


def graph(gain):
    """Find every cycle of the map y -> y + gain[y] modulo SIZE."""
    visited = set()
    cycles = []
    for y in range(SIZE):
        if y in visited:
            continue
        order = {}
        while y not in visited and y not in order:
            order[y] = len(order)
            y = (y + gain[y]) % SIZE
        if y in order:
            cycles.append(list(order)[order[y]:])
        visited.update(order)
    return cycles


def counts(padding):
    """Seven ordinary pairs, then the padding jumps and one final bulk."""
    flags = []
    for initial_d in range(SIZE):
        d = initial_d
        high = 0
        for _ in range(7):
            r = d % 4
            high += (PAIR_U[r] - 5) // 2
            d = (9*d + PAIR_D[r]) // 4
        # Initial u odd, then seven odd gains. At the padding jumps u
        # stays even, so d'=3d-u+1 flips its low bit on every jump.
        flags.append(high + (d + padding) % 2)
    return flags


def check_row(m, step, padding, target_phase, length, winding):
    assert step % SIZE == 0
    gain = [m + 20 + padding + b for b in counts(padding)]
    cycle, = graph(gain)
    assert len(cycle) == length and target_phase in cycle
    assert sum(gain[y] for y in cycle) == SIZE * winding
    slope = length * (step // SIZE)
    assert gcd(winding, slope) == 1
    print(m, step, target_phase, length, winding, slope)


def main():
    upper = 1 + Fraction(2*CUSP_Q, CUSP_DEN)
    right = upper - 1 + Fraction(1, 10000)
    for i in range(15):
        assert 2 - (3*Fraction(3, 2)**i - 2)*right > 0
    assert 2 - 2*(Fraction(3, 2)**15 - 1)*right > 0
    assert 2 - (3*Fraction(3, 2)**15 - 2)*(upper - 1) == 0
    cusp_step = 19660800
    for m, sibling, length, winding in ((36597, 1, 1368, 1529),
                                        (350997, 0, 153, 1639)):
        assert m % 1200 == 597 and cusp_step % 1200 == 0
        target_phase = (2*BASE_I - 1 + sibling) % SIZE
        check_row(m, cusp_step, 0, target_phase, length, winding)

    m, step = 242417632, 15902965760
    assert m % 242660 == 292 and step % 242660 == 0
    assert step % (8*SIZE) == 0
    mod = 2 * SIZE
    seed = ((pow(3, m+15, mod) - H_OFFSET)*pow(H_DEN, -1, mod) - 2*m) % mod
    assert seed == 57901
    phase = ((seed - pow(3, m, mod)) // 2 + m) % SIZE
    check_row(m, step, 13, phase, 3879, 28696843)


if __name__ == '__main__':
    main()
