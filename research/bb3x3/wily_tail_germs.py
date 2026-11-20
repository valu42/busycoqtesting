"""Classify the recurrent carry pairs on an untouched Wily tail."""
import argparse
from itertools import product

from check_bb33 import WILY
from wily_integer_map import START, canonical_bucket, image, inverse
from wily_edge_stream import append_run, through


def paired(carries, bit):
    left, right = carries
    middle, new_left = WILY.rules[left][bit]
    last, new_right = WILY.rules[right][middle]
    return (new_left, new_right), last


def flip(n):
    return n + 3*(1 - 2*(n % 2))


def carry1(n):
    if n % 2:
        return 2*image((n-3)//2)
    return 3+2*flip(n//2)


def product_value(n, start):
    # U is chronological (s0,s1), V is (s1,s0).
    return carry1(image(n)) if start == 0 else image(carry1(n))


def discrepancy(n, start, count):
    """Closed action of U^count or V^count on any eventually alternating input."""
    tail = n
    prefix = width = 0
    expected = start
    while True:
        bit = tail % 2
        if tail == (-1 if expected else -2):
            return n
        prefix += (3*bit) << width
        width += 1
        tail = (tail-3*bit)//2
        if bit != expected:
            break
        expected ^= 1
    # A mismatch 1 in U leaves J F J, a mismatch 0 in V leaves F.
    if bit:
        tail = flip(tail)
    for _ in range(count):
        tail = image(tail)
    if bit:
        tail = flip(tail)
    return prefix + (tail << width)


def check_early_blank_sections():
    carries = [(0,1)]
    n = START
    for width in range(69):
        if width:
            # A 0-run of length at least two includes a 3.
            assert any(m in (2,3) or (m == 0 and count > 1) for m,count in carries)
        bit = n % 2
        n = (n-3*bit)//2
        output, final = through(carries,bit)
        if final != bit:
            other, restored = through(carries,final)
            assert restored == bit
            for mode, count in other:
                append_run(output,mode,count)
        carries = output
    assert n == -1
    assert WILY.rules[3][1] == (0,-1) and WILY.rules[0][0] == (1,1)
    assert WILY.rules[1][0] == (1,3) and WILY.rules[0][1] == (0,2)


def check_blank_counts(limit):
    carries = [(0,1)]
    n = START
    candidates = []
    for width in range(limit+1):
        counts = [0]*4
        for m, count in carries:
            if m in (1,2):
                counts[m] += count
            else:
                counts[m] += (count+1)//2
                counts[3-m] += count//2
        if counts[1] == counts[0]+counts[2]:
            candidates.append(width)
            word = [m if m in (1,2) or i%2 == 0 else 3-m
                    for m,count in carries for i in range(count)]
            def action(value):
                for mode in word:
                    if mode == 0:
                        value = image(value)
                    elif mode == 1:
                        value = carry1(value)
                    elif mode == 2:
                        value = image(flip(value))
                    else:
                        value = flip(value)
                return value
            for start in (0,1):
                assert any(action(v) != discrepancy(v,start,counts[1])
                           for v in range(1,128) if v % 3)
        bit = n % 2
        n = (n-3*bit)//2
        output, final = through(carries,bit)
        if final != bit:
            other, restored = through(carries,final)
            assert restored == bit
            for mode, count in other:
                append_run(output,mode,count)
        carries = output
    return candidates


def check_prefix_period_bound():
    # Signatures are (root flip, count of mode 0 or 2, count of mode 1).
    signatures = [(1, 1, 0), (1, 0, 1), (0, 1, 0), (1, 0, 0)]
    for mode, (_, a, b) in enumerate(signatures):
        sections = [signatures[t] if t != -1 else (0, 0, 0) for _, t in WILY.rules[mode]]
        assert all((flip ^ ones) == b for flip, _, ones in sections)
        assert tuple(left ^ right for left, right in zip(*sections)) == (a, a ^ b, a)
    for width in range(15):
        size = 1 << width
        limit = 1 << (1 + 2*width//3) if width else 1
        mask = size - 1
        visited = set()
        for start in range(size):
            if start in visited:
                continue
            n, period = start, 0
            while n not in visited:
                visited.add(n)
                # A unit representative with this low prefix of the numerator.
                n = image(n if n % 3 else n + size) & mask
                period += 1
            assert n == start and limit % period == 0
    for e in range(-4096, 0):
        if e % 3 == 0 or image(e) <= 0:
            continue
        width = canonical_bucket(e).bit_length()-1
        n = e
        for _ in range(1 << (1 + 2*width//3)):
            n = inverse(n)
            if n > 0:
                break
        assert n > 0


def check_large_prefix_period():
    # z is the ordinary little-endian bit integer of the tested prefix.
    z = 1_317_624_506_749_325_312
    carries = [(0, 1)]
    power = 0
    for width in range(63):
        bit = (z >> width) % 2
        output, final = through(carries, bit)
        doubled = final != bit
        assert doubled == (width < 3 or width % 3 != 0)
        if doubled:
            other, restored = through(carries, final)
            assert restored == bit
            for mode, count in other:
                append_run(output, mode, count)
            power += 1
        carries = output
    assert power == 43


def main():
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts", action="store_true", help="test all blank sections through 350 bits")
    args = parser.parse_args()
    pairs = set(product(range(3),repeat=2))
    graph = {p:{q for bit in range(2) for q,_ in [paired(p,bit)] if q in pairs}
             for p in pairs}
    reach = {p:set(v) for p,v in graph.items()}
    for p in pairs:
        for q in pairs:
            if p in reach[q]:
                reach[q].update(reach[p])
    cycles = {p for p in pairs if p in reach[p]}
    assert cycles == {(2,2),(0,1),(1,0)}
    assert all(paired(p,b)==(q,b) for p,b,q in
               (((2,2),0,(2,2)), ((0,1),0,(1,0)), ((1,0),1,(0,1))))
    assert graph[(0,1)] == {(1,0)} and graph[(1,0)] == {(0,1)}
    assert graph[(2,2)] == {(2,2),(1,1)} and not graph[(1,1)]
    # Every infinite run enters a recurrent component within three columns.
    viable = set(pairs)
    for _ in range(len(pairs)):
        viable = {p for p in pairs if graph[p] & viable}
    layer = viable-cycles
    for _ in range(3):
        layer = {q for p in layer for q in graph[p] if q in viable-cycles}
    assert not layer
    check_early_blank_sections()
    check_prefix_period_bound()
    if args.counts:
        check_large_prefix_period()
        assert check_blank_counts(350) == [1,14,34]
        print("Excluded both alternating products algebraically through all 350 blank cutoffs.")
    for n in range(-1024,1025):
        if not n % 3:
            continue
        for start in (0,1):
            target = n
            for t in range(9):
                assert discrepancy(n,start,t) == target
                target = product_value(target,start)
    print("Checked the three recurrent pair states and both discrepancy rules in both alternating phases.")


if __name__=="__main__":
    main()
