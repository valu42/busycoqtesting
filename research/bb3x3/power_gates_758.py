"""Reconstruct the exact reset checkpoints at powers of three for #758."""
import argparse
import heapq
from pathlib import Path
from check_bb33 import champion_step, first_return

MANIFEST = Path(__file__).with_name("power_gates_758.tsv")


def coarse_return(m, seed, multiple):
    """Replay the predicted post-prefix branches and verify their exact guards."""
    p = 3**m
    q = p//3
    if multiple == 2 and seed % 2:
        a, c, word = 2*p-1, seed-p+1+2*m, "L"
    elif seed % 2:
        a, c, word = 2*q-1, seed-q+1+2*(m-1), "L"
    else:
        a, c = 4*q-1, seed-2*q+2*m+3
        word = "L" if multiple == 2 else "LLJLLL"
    # These formulas batch only an initial string of Js (following I for
    # even seeds). Positivity of the final c suffices for every earlier guard.
    assert c >= 1 and c % 2 and a > 1
    for branch in word:
        if branch == "L":
            assert a >= 4*((c+1)//4)+3
        else:
            assert a % 2 and a <= c
        a, c = champion_step(a, c)
        assert a != 1
    assert a % 2 == 0 and a <= c
    return a//2 + c + 2


def section_index(m, seed):
    """Index of the actual post-bulk state in a doubled-to-next-power gap."""
    p = 3**m
    assert 2*p-2*m-4 <= seed <= 3*p-2*m-6
    if seed % 2:
        seed += 2*m+5+2*(seed%4 == 3)
    return (seed-2*p+2*m+6)//4


def check_section(m):
    """Check the algebraic common states against the original map."""
    p = 3**m
    for base in (2*p-2*m-4, 5*p//2, 3*p-2*m-9):
        for s in range(base, base+4):
            i = section_index(m,s)
            even = s if s%2==0 else first_return(s)
            assert even is not None and even%2==0
            a,c = 1,even
            for _ in range(m+2):  # I, m Js, one L
                a,c = champion_step(a,c)
            assert (a,c) == (4*p-4*i-4,6*i+5)
            assert a+2*c == 4*p+8*i+6


def gate_exits(m, multiple):
    p = 3**m
    margin = 34*(4*m+40)
    if multiple == 1:
        low = (9999*p+9999)//10000
        cut = p-2*m-4  # last odd seed with the short word
        upper = (cut+2*m+7, cut)
    else:
        low = (19*p+9)//10
        cut = 2*p-2*m-6  # last even seed with the short word
        upper = (cut, cut+2*m+11)
    assert low + 50_000 < cut-margin
    if multiple == 2:
        # The odd short word continues all the way to the next odd-power
        # boundary, eliminating every odd excursion from the inter-gate gap.
        rightmost = 3*p-2*m-6
        assert rightmost % 2 == 1
        for seed in (low+(1-low)%2, rightmost):
            result = coarse_return(m, seed, 2)
            assert result-seed == 2*m+5+2*(seed%4 == 3)
    for parity in range(2):
        left = low + (parity-low) % 2
        right = upper[parity] - (upper[parity]-parity) % 2
        for seed in (left, right):
            assert coarse_return(m, seed, multiple) > seed

    # Within the short words, adding 64 to a seed preserves all bulk
    # residues. Each L loses one of the six low bits and there are at most
    # five Ls. Therefore the seed increment depends on the residue alone.
    base = low + (-low) % 64
    gains = [coarse_return(m, base+r, multiple)-(base+r) for r in range(64)]
    assert all(d > 0 and d % 2 for d in gains)
    if multiple == 2:
        for r, g in enumerate(gains):
            expected = (2*m+5+2*(r%4 == 3) if r%2 else
                        2*m+7+2*((r+2*m)%4 == 2))
            assert g == expected
        return tuple(cut+2+4*i for i in range(m+4))

    assert max(gains[0::2]) <= 2*m+29 and max(gains[1::2]) <= 2*m+5
    odd = set(range(1, 64, 2))
    pairs = {r: gains[r]+gains[(r+gains[r])%64] for r in odd}
    cycle = odd
    for _ in range(32):
        cycle = {(r+pairs[r])%64 for r in cycle}
    assert {(r+pairs[r])%64 for r in cycle} == cycle
    assert max(gains)+32*max(pairs.values()) < margin
    exits = set()
    for r in cycle:
        s = cut-(cut-r)%64
        while s+pairs[r] > cut:
            exits.add(s+pairs[r])
            s -= 64
    return tuple(sorted(exits))


def coalesce(seeds, budget):
    live = set(seeds)
    heap = list(live)
    heapq.heapify(heap)
    steps = 0
    while len(live) > 1:
        assert steps < budget
        seed = heapq.heappop(heap)
        live.remove(seed)
        nxt = first_return(seed)
        assert nxt is not None and nxt > seed
        if nxt not in live:
            heapq.heappush(heap, nxt)
            live.add(nxt)
        steps += 1
    return heap[0], steps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true', help='replay all 546 mergers')
    group.add_argument('--m', type=int, choices=range(20, 293), metavar="20..292")
    args = parser.parse_args()
    selected = {32, 292} if args.m is None else {args.m}
    # The first unlinked odd gate can be entered earlier than its uniform
    # 9999/10000 cutoff. These are the first successful seeds of each parity.
    for parity, first in ((0, 5_494_990_037_991_760), (1, 3_335_436_339_933_247)):
        assert first % 2 == parity
        assert coarse_return(33, first, 1) > first
        try:
            coarse_return(33, first-2, 1)
        except AssertionError:
            pass
        else:
            raise AssertionError("the preceding seed still has the requested word")
    checked = 0
    with MANIFEST.open() as file:
        assert next(file).split() == ['m', 'multiple', 'exits', 'edges', 'offset']
        rows = [tuple(map(int, line.split())) for line in file]
    assert [(m,k) for m,k,*_ in rows] == [(m,k) for m in range(20,293) for k in (1,2)]
    for m, k, count, edges, offset in rows:
        if k == 2:
            check_section(m)
        exits = gate_exits(m,k)
        assert len(exits) == count
        if args.all or m in selected:
            checkpoint, steps = coalesce(exits, edges)
            assert (checkpoint-k*3**m, steps) == (offset, edges)
            checked += 1
            if not args.all:
                print(f"m={m}, multiple={k}: {count} exits meet at offset {offset:,}")
    print(f"Confirmed 546 exit sets and replayed {checked} mergers.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    main()
