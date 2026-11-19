"""Certify a conditional #758 raw-time lower bound by integer inequalities."""
from decimal import Decimal

from check_bb33 import HALTING_TARGET, champion_step
from timing_758 import branch_cost


BINS = 256
MARGIN = 4
MIN_MASS = 10**10
MAX_TARGET = 2 * HALTING_TARGET + 1
SCALE = 4 * BINS**2
DENOMINATOR = 12_500
LOW, HIGH = 2 * BINS, 2 * BINS + 1
LOW_GAIN = 4 * 293 + 13
HIGH_GAIN = 9 * 787


def make_graph():
    """Edges store a lower cost in units of W²/SCALE and a mass gain ceiling."""
    edges = [dict() for _ in range(HIGH + 1)]

    def add(source, dest, charge, gain):
        if dest in edges[source]:
            old_charge, old_gain = edges[source][dest]
            assert old_charge == charge
            gain = max(old_gain, gain)
        edges[source][dest] = charge, gain

    def add_range(source, first, last, parity, charge, gain):
        if first < MARGIN:
            add(source, LOW, charge, gain)
        if last >= BINS - MARGIN:
            add(source, HIGH, charge, gain)
        for j in range(max(MARGIN, first), min(BINS - MARGIN - 1, last) + 1):
            add(source, 2*j + parity, charge, gain)

    for i in range(MARGIN, BINS - MARGIN):
        charge = 3 * min(2*i, BINS-i-1)**2
        if 3*i <= BINS:
            add(2*i, LOW, charge, 5)
            add_range(2*i+1, 3*i-1, 3*(i+1), 1, charge, 4)
        if 3*(i+1) > BINS:
            for parity in (0, 1):
                add_range(2*i+parity, (3*i-BINS)//2-1, (3*(i+1)-BINS)//2,
                          1-parity, charge, 9)
        if 3*i <= BINS+1 and 3*(i+1) > BINS:
            add(2*i+1, HIGH, charge, 8)

    for j in range(MARGIN, 3*MARGIN+1):
        add(LOW, 2*j+1, 0, LOW_GAIN)
    for j in range(BINS-(3*MARGIN+1)//2-1, BINS-MARGIN):
        for parity in (0, 1):
            add(HIGH, 2*j+parity, 0, HIGH_GAIN)
    return edges


def certify_potential(edges):
    """Find an integer vertex potential and check every edge independently."""
    values = [0] * len(edges)
    for _ in edges:
        changed = False
        for source, row in enumerate(edges):
            for dest, (charge, gain) in row.items():
                candidate = values[source] + DENOMINATOR*charge - SCALE*gain
                if candidate < values[dest]:
                    values[dest] = candidate
                    changed = True
        if not changed:
            break
    for source, row in enumerate(edges):
        for dest, (charge, gain) in row.items():
            assert DENOMINATOR*charge >= SCALE*gain + values[dest] - values[source]
    assert max(values) == 0
    return -min(values)


def lower_at_mass(target, potential_range):
    """Lower bound through first crossing of target, for the indicated range."""
    if not MIN_MASS + 2*HIGH_GAIN + 8 <= target <= MAX_TARGET:
        raise ValueError("mass lies outside the certified range")
    span = (target - 2*HIGH_GAIN)**3 - (MIN_MASS + 8 - HIGH_GAIN)**3
    return (SCALE*span - 3*potential_range*(target+8)**2) // (3*SCALE*DENOMINATOR)


def vertex(a, c):
    i = BINS*a // (a + 2*c)
    if i < MARGIN:
        return LOW
    if i >= BINS - MARGIN:
        return HIGH
    return 2*i + a%2


def audit_literals(edges):
    """Check angular boundaries, exceptional rules, and full axis visits."""
    def check(a, c):
        source = vertex(a, c)
        initial_mass = a + 2*c
        raw = 0
        for _ in range(800):
            raw += branch_cost(a, c)
            state = champion_step(a, c)
            if state is None:
                return
            a, c = state
            dest = vertex(a, c)
            if source < LOW or dest != source:
                charge, gain = edges[source][dest]
                assert raw*SCALE >= charge*initial_mass**2
                assert a + 2*c - initial_mass <= gain
                return
        raise AssertionError("axis visit exceeded bound")

    for mass in (MIN_MASS + 100, 10**30, MAX_TARGET - 10**8):
        for i in range(BINS+1):
            for offset in range(-4, 5):
                a = max(0, min(mass-2, i*mass//BINS + offset))
                c = max(1, (mass-a)//2) | 1
                check(a, c)
        for d in range(6):
            c = ((mass//3) | 1) - 2
            check(c+d, c)
            check(c+d-2, c-2)
        check(1, mass//2 - (mass//2)%2)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable the certificate checks.")
    assert 13 * BINS < MIN_MASS
    assert 3**294 > MAX_TARGET+9
    assert 16*3**788 > (MAX_TARGET+8+14)*2**788
    graph = make_graph()
    potential_range = certify_potential(graph)
    audit_literals(graph)
    result = lower_at_mass(MAX_TARGET-4, potential_range)
    assert result - 50_707 > 210*10**412
    print("edges", sum(map(len, graph)), "potential range", potential_range)
    print("lower bound for either candidate mass in #758", result)
    print("scientific notation", format(Decimal(result), ".12E"))
