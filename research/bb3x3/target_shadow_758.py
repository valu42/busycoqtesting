#!/usr/bin/env python3
"""Exact, right-continuous rational itinerary below the known halting target."""
from fractions import Fraction
from random import Random
from check_bb33 import champion_step
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word
from scale_transport_758 import prefix

D = 13_959_275
POWER = 3**307
C = 8_282_708_212
LOW, HIGH = 10**4, 10**64


def horizon(upper):
    """A guard at elementary depth l needs at most another two powers of 3."""
    t = 307
    while 3**(307-t) <= D*(upper+2000):
        t -= 1
    return t-2


def aligned(distance):
    if not LOW <= distance <= HIGH or distance % 2:
        raise ValueError("odd reset required in the proven distance range")
    twice_h, gain = prefix(distance)
    h, u = twice_h//2, H-distance+gain//2
    k = 0
    while 3*h <= u+2:
        h, u, k = 3*h, u+2, k+1
    return h, u, k


def prediction(distance, budget):
    """Yield the coarse decision at every reached grouped depth through budget."""
    h, u, k = aligned(distance)
    p, q = D*h, POWER
    used = 0
    while used <= budget:
        if 3*p < q:
            yield used, "J"
            p *= 3
            used += 1
        elif 9*p < 5*q:
            yield used, "R"  # one bulk, then the ordinary reset
            return
        else:
            yield used, "P"
            p, q = 9*p-5*q, 4*q
            used += 2


def literal(distance, budget):
    h, u, _ = aligned(distance)
    a, c = 2*h-1, u-h+1
    used = 0
    while used <= budget:
        assert a > 1 and a % 2 and c % 2
        if a <= c:
            yield used, "J"
            a, c = champion_step(a, c)
            used += 1
        else:
            assert a >= 4*((c+1)//4)+3, (distance, used, a, c)
            a, c = champion_step(a, c)
            if a <= c:
                assert not a % 2 and c % 2 and champion_step(a,c)[0] == 1
                yield used, "R"
                return
            assert a >= 4*((c+1)//4)+3 and not a % 2
            a, c = champion_step(a,c)
            yield used, "P"
            used += 2


def verify():
    assert H*D == POWER-C
    # With fixed parity, each prefix letter preserves the ordering of the
    # two opposite counter coordinates. The final left coordinate is largest
    # at HIGH. The complete prefix at both endpoints has no intermediate reset.
    for d in (LOW,HIGH):
        check_word(H-d, PREFIX)
    for d in (LOW+1,HIGH-1):
        check_word(H-d, EVEN_WORD)
    max_h0 = prefix(HIGH)[0]//2
    assert H-HIGH > 3*max_h0*D*(HIGH+2000)
    assert 3**293 > H+2000
    assert Fraction(C,D) > 593 and Fraction(C,D) < 594
    assert (horizon(HIGH), horizon(2_716_248_271_952_006)) == (155,257)

    rng = Random(758)
    distances = set(range(LOW, LOW+20_000, 2))
    for power in range(28,139):
        center = 3**power
        distances.update(d for j in range(-16,17) if LOW <= (d := 2*(center//2+j)) <= HIGH)
    for _ in range(5000):
        scale = 10**rng.randrange(5,65)
        distances.add(2*rng.randrange(LOW//2,scale//2+1))
    distances.add(HIGH)
    longest = (0,0)
    for d in distances:
        limit = horizon(d)
        path = list(prediction(d, limit))
        assert path == list(literal(d, limit)), d
        longest = max(longest,(path[-1][0],d))
    print(f"{len(distances)} exact itineraries checked; latest tested guard at depth {longest[0]}.")
    print("Guaranteed guard depths:", horizon(HIGH), horizon(2_716_248_271_952_006))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    verify()
