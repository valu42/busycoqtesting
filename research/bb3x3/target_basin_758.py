#!/usr/bin/env python3
"""Certify the physical endpoints and induction for the dyadic halting-basin proof."""
import argparse
from collections import defaultdict
from pathlib import Path
from math import comb
import re
import subprocess

from header_tail_ancestry_758 import compatible_offsets
from check_bb33 import champion_step
from lower_scale_gates_758 import GATES
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word
from target_shadow_758 import aligned, horizon

NEAR = 3_403_055
OLD_FAR = GATES[7][1]
# n, closest/farthest even distance on the new outer simple-word corridor.
GATES_NEW = {
    11: (1_629_748_963_171_204, 2_716_248_271_952_006),
    12: (4_889_246_889_513_612, 8_148_744_815_856_018),
    13: (14_667_740_668_540_832, 24_446_234_447_568_050),
    14: (44_003_222_005_622_492, 73_338_703_342_704_146),
    15: (132_009_666_016_867_464, 220_016_110_028_112_434),
    16: (396_028_998_050_602_388, 660_048_330_084_337_306),
    17: (1_188_086_994_151_807_156, 1_980_144_990_253_011_922),
    18: (3_564_260_982_455_421_460, 5_940_434_970_759_035_762),
    19: (10_692_782_947_366_264_372, 17_821_304_912_277_107_282),
}
HERE = Path(__file__).resolve().parent


def physical(n):
    near,far = GATES_NEW[n]
    # Each fixed-length launch word holds on an interval of ordered inputs.
    for d in (OLD_FAR, near-2):
        check_word(H-d,PREFIX)
    for d in (OLD_FAR+1, far-1):
        check_word(H-d,EVEN_WORD)
    k_hi, k_lo = (aligned(d)[2] for d in (OLD_FAR, near-2))
    r_lo,r_hi = 307-k_hi,307-k_lo
    assert (r_lo,r_hi) == (50,n+42)
    for d in (near,far):
        check_word(H-d,PREFIX+'J'*(264-n)+'LR')
    assert horizon(near-2) >= (257 if n==11 else 250)
    assert 9*(307+k_hi+257+2)//2 < 4000 < 9000 < OLD_FAR-NEAR
    return r_lo,r_hi,far


def check_exception(distance):
    """Follow the full counters for a rare compatible numerator if necessary."""
    state = 1,H-distance
    for _ in range(2_000):
        state = champion_step(*state)
        if state is None:
            return
        if state[0] == 1:
            assert 0 < state[1]-(H-distance) <= 9_000
            return
    raise AssertionError(f"Unresolved physical header at distance {distance}")


def run(*args):
    return subprocess.check_output(list(map(str,args)), text=True)


def read_tails(max_pairs):
    rows = defaultdict(dict)
    lines = (HERE/'dyadic_long_tails_758.tsv').read_text().splitlines()
    assert lines[0].split() == ['p','numerator','length']
    for line in lines[1:]:
        p,n,length = map(int,line.split())
        if p > max_pairs:
            continue
        assert p >= 24 and 0 < n < 4**p and n%10 == 5 and n not in rows[p]
        a,b,depth = n,4**p,0
        while depth < length:
            if 3*a < b:
                a,depth = 3*a,depth+1
            else:
                assert 9*a > 5*b
                a,b,depth = 9*a-5*b,4*b,depth+2
        assert length >= 189 and depth == length and 3*a > b and 9*a < 5*b
        rows[p][n] = length
    assert all(rows[p] for p in range(24,max_pairs+1))
    return rows


def check_dyadics(worker, join, max_pairs, expected):
    small = min(max_pairs,25) if join else max_pairs
    maxima = {}
    observed = defaultdict(dict)
    for line in run(worker,1,small,240).splitlines():
        if line.startswith('long_tail '):
            _,p,n,depth = line.split()
            observed[int(p)][int(n)] = int(depth)
        match = re.search(r'p=(\d+) max=(\d+).*censored=(\d+) deepest_split=(\d+)',line)
        if match:
            p,maximum,censored,split = map(int,match.groups())
            assert p not in maxima and censored==0 and split<189
            maxima[p] = maximum
    assert set(maxima) == set(range(1,small+1))
    assert max(maxima[p] for p in range(1,24)) == 187
    for p in range(small+1,max_pairs+1):
        # b determines the number of letters on each side of the join.
        b,bits = {26:(23,32),27:(25,36),28:(26,35)}[p]
        for line in run(join,p,b,189,bits).splitlines():
            if line.startswith('long_tail '):
                _,reported,n,depth = line.split()
                assert int(reported)==p
                observed[p][int(n)] = int(depth)
    for p in range(1,max_pairs+1):
        assert observed[p] == expected[p], p


def high_receipts():
    rows = {}
    for line in (HERE/'high_pair_headers_758.tsv').read_text().splitlines()[1:]:
        r,p,limit,*fields = map(int,line.split())
        assert (r,p) not in rows and fields[-1] == 0
        # First P is fixed. When a pair straddles r the last P is also fixed.
        cells = comb(r-p-1,p-1) + comb(r-p-1,p-2)
        assert fields[0] == cells and cells > 0
        rows[r,p] = (limit,*fields)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale',type=int,choices=GATES_NEW,default=max(GATES_NEW))
    parser.add_argument('--dyadic',type=Path,help='rerun the full dyadic enumeration')
    parser.add_argument('--headers',type=Path,help='rerun the high-pair header checks')
    parser.add_argument('--join',type=Path,help='use the faster two-sided dyadic checker above p=25')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with integer assertions enabled')
    if bool(args.dyadic) != bool(args.headers) or args.join and not args.dyadic:
        parser.error('supply both --dyadic and --headers for exhaustive replay')
    lo,hi,far = physical(args.scale)
    receipts = high_receipts()
    minimum = {r:min(p for rr,p in receipts if rr==r) for r in range(lo,hi+1)}
    max_pairs = max(minimum.values())-1
    if args.dyadic and max_pairs > 27 and not args.join:
        parser.error("scale 19 needs --join to verify the p=28 directions")
    tails = read_tails(max_pairs)
    if args.dyadic:
        check_dyadics(args.dyadic.resolve(),args.join.resolve() if args.join else None,max_pairs,tails)

    rare = set()
    for r in range(lo,hi+1):
        limit = 257 if r<=53 else 250
        assert r+1+188 <= limit
        near = GATES_NEW[11 if r<=53 else args.scale][0]
        if r<=53:
            assert aligned(near)[2] == 253
        assert horizon(near-2) >= limit
        for p in range(24,minimum[r]):
            # Every direction that could outlast the angular proof is on this list.
            # Checking the entire list also makes the exceptional replays reproducible.
            origins = compatible_offsets(r,p,tails[p])
            for offsets in origins.values():
                for distance in offsets:
                    if OLD_FAR <= distance <= GATES_NEW[args.scale][0]-2 and aligned(distance)[2]==307-r:
                        check_exception(distance)
                        rare.add(distance)
        expected = []
        for p in range(minimum[r],(r+1)//2+1):
            guard,*fields = receipts[r,p]
            assert guard == limit
            expected.append((r,p,guard,*fields))
        if args.headers:
            lines = run(args.headers.resolve(),r,r,minimum[r],limit).splitlines()
            actual = [tuple(map(int,l.split())) for l in lines if l[:1].isdigit()]
            assert actual == expected
    print(f'Checked {lo}..{hi} denominator exponents and {len(rare)} rare physical offsets.')
    if not args.dyadic:
        print('Using archived exhaustive results; supply the compiled workers for a full replay.')
    print(f'All {far-NEAR+1:,} reset starts with {NEAR:,} <= H-s <= {far:,} halt.')


if __name__ == '__main__':
    main()
