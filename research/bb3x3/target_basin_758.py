#!/usr/bin/env python3
"""Certify the physical endpoints and induction for the dyadic halting-basin proof."""
import argparse
from collections import defaultdict
from pathlib import Path
from math import comb
import re
import subprocess

from dyadic_guard_shadow_758 import guard_counts
from fractions import Fraction
from lower_scale_gates_758 import GATES
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word
from target_shadow_758 import D, POWER, aligned, horizon
from scale_transport_758 import BETA_LOW, PERIOD, SLOPE

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
    20: (32_078_348_842_098_793_108, 53_463_914_736_831_321_850),
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
    assert horizon(near-2) >= (257 if n==11 else 249 if n==20 else 250)
    # The longest listed tail takes 243 calls after a cut at depth at most 63.
    assert 9*(len(PREFIX)+k_hi+r_hi+1+243+2) < 2*4000 < 2*(OLD_FAR-NEAR)
    return r_lo,r_hi,far


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
        assert 189 <= length <= 243
        rows[p][n] = length
    expected_counts = {24:3, 25:8, 26:37, 27:176, 28:748}
    assert all(len(rows[p])==expected_counts[p] for p in range(24,max_pairs+1))
    return rows


def least_tail_margin(tails):
    """Minimum aligned clearance, in units of U/3^m, on every listed tail."""
    minimum = None
    for p, group in tails.items():
        for numerator, length in group.items():
            final_triple = 3**length
            a, b, triple = numerator, 4**p, 1
            while True:
                # Nine times the distance to the closest of 0, 1/3, 5/9, 1
                # after clearing the current power-of-four denominator.
                gap = min(9*a, 3*abs(3*a-b), abs(9*a-5*b), 9*(b-a))
                assert gap > 0
                if minimum is None or gap*minimum.denominator < 9*triple*minimum.numerator:
                    minimum = Fraction(gap, 9*triple)
                if 3*a < b:
                    a, triple = 3*a, 3*triple
                elif 9*a > 5*b:
                    a, b, triple = 9*a-5*b, 4*b, 9*triple
                else:
                    break
                assert triple <= final_triple
            assert triple == final_triple
    return minimum


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
        parser.error("scales 19 and 20 need --join to verify the p=28 directions")
    tails = read_tails(max_pairs)
    if args.dyadic:
        check_dyadics(args.dyadic.resolve(),args.join.resolve() if args.join else None,max_pairs,tails)

    margin = least_tail_margin(tails)
    if margin is not None:
        clearance = POWER*margin/(D*3**(hi+1))
        assert clearance > GATES_NEW[args.scale][0]+2000
        print(f'Listed tails clear every physical guard by at least {int(clearance):,} aligned units.')
        # The existing affine header bound gives 2*PERIOD*h0 >= SLOPE*d+BETA_LOW.
        # A pre-aligned h0 subsequently grows to h<U in the physical shadow range.
        r = 106
        max_distance = (2*PERIOD*3**r-D*BETA_LOW)//(D*SLOPE)
        assert POWER*margin > D*3**(r+1)*(max_distance+2000)

    for r in range(lo,hi+1):
        high_guard = 257 if r<=53 else 249 if r==62 else 250
        # k is nonincreasing in d. At upper+2 the exponent has increased,
        # so upper bounds every even distance with the exponent under test.
        upper = GATES_NEW[max(11,r-42)][0]-2
        assert 307-aligned(upper)[2] == max(53,r)
        assert 307-aligned(upper+2)[2] == max(53,r)+1
        uniform = horizon(upper)
        assert uniform >= high_guard
        last_short = r+1+188
        if last_short > uniform:
            extra = list(guard_counts(r,upper,last_short))
            assert extra and all(ancestors==0 for _,_,ancestors in extra)
        limit = high_guard
        expected = []
        for p in range(minimum[r],(r+1)//2+1):
            guard,*fields = receipts[r,p]
            assert guard == limit
            expected.append((r,p,guard,*fields))
        if args.headers:
            lines = run(args.headers.resolve(),r,r,minimum[r],limit).splitlines()
            actual = [tuple(map(int,l.split())) for l in lines if l[:1].isdigit()]
            assert actual == expected
    print(f'Checked denominator exponents {lo} through {hi}.')
    if not args.dyadic:
        print('Using archived exhaustive results; supply the compiled workers for a full replay.')
    print(f'All {far-NEAR+1:,} reset starts with {NEAR:,} <= H-s <= {far:,} halt.')


if __name__ == '__main__':
    main()
