"""Exclude reset ancestry for periodic directions at the #758 central crossing."""
from fractions import Fraction
from itertools import product

from check_cut_residues import CUT
from terminal_forest_758 import exhaust
from verify_cut import lift


def directions(max_period):
    """Fixed points of the frozen inverse maps J(x)=(x+1)/3, P(x)=4x/9."""
    found = set()
    for length in range(2, max_period+1):
        for word in product("JP", repeat=length):
            if len(set(word)) != 2:
                continue
            a, c, m = 1, 0, 1
            for letter in reversed(word):
                if letter == "J":
                    c += m
                    m *= 3
                else:
                    a *= 4
                    c *= 4
                    m *= 9
            slope = Fraction(c, m-a)
            if slope not in found:
                found.add(slope)
                yield slope


def ancestors(u, d):
    target = (2*u - 4*d - 1, 2*d + 1)
    # Hitting this resource limit raises an exception; it cannot pass a test.
    resets, nodes, depth = exhaust(target, 10_000)
    assert not resets
    return nodes, depth


def sharp_witnesses():
    expected = ((2, 1), (463, 85), (885, 147), (1183, 209), (1853, 278))
    for h, answer in zip((0, 23, 46, 69, 92), expected):
        j = 98 - h
        d, rem = divmod(92*CUT - 900 + 12*27**h * 4**j, 529)
        assert rem == 0
        assert ancestors(CUT, d) == answer
    print("All five 98-copy cut witnesses have zero reset ancestors.")


def mixed_witnesses():
    # At the central cut, construct a root with 72 specified blocks on
    # each side (the B in this constructor specifically means two b updates).
    from random import Random

    words = ["J"*144, "B"*144, "JB"*72, "BJ"*72]
    words += ["".join(Random(i).choices("JB", k=144)) for i in range(1024)]
    total = max_nodes = max_depth = 0
    for word in words:
        prefix = word[:72]
        u = CUT - 2*prefix.count("J") - 5*prefix.count("B")
        d, _ = lift(u, word)
        for letter in prefix:
            if letter == "J":
                u, d = u+2, 3*d-u+1
            else:
                u, d = u+5, (9*d+20)//4
        assert u == CUT
        nodes, depth = ancestors(u, d)
        total += nodes
        max_nodes = max(max_nodes, nodes)
        max_depth = max(max_depth, depth)
    assert (total, max_nodes, max_depth) == (708138, 1316, 152)
    print("All 1,028 two-sided 144-block witnesses have zero reset ancestors.")


def all_short_periods():
    # The diameter of the 395-block frozen inverse image is <1 at every
    # normalized odd mass of the cut. The proved 14-unit error then suffices.
    assert (CUT+8)*4**395 < 2*9**395
    count = total = max_nodes = max_depth = 0
    for slope in directions(13):
        for u in range(CUT, CUT+9):
            center = u*slope.numerator // slope.denominator
            for d in range(center-14, center+16):
                nodes, depth = ancestors(u, d)
                count += 1
                total += nodes
                max_nodes = max(max_nodes, nodes)
                max_depth = max(max_depth, depth)
    assert (count, total, max_nodes, max_depth) == (4379400, 32925469, 658, 93)
    print("All 4,379,400 periodic-direction tests have zero reset ancestors.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so verification checks execute.")
    sharp_witnesses()
    mixed_witnesses()
    all_short_periods()
