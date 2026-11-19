#!/usr/bin/env python3
"""Certify the physical endpoints and induction for the dyadic halting-basin proof."""
import argparse
from pathlib import Path
import re
import subprocess

from lower_scale_gates_758 import GATES
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word
from target_shadow_758 import aligned, horizon

NEAR = 3_403_055
OLD_FAR = GATES[7][1]
# n, closest/farthest even distance on the new outer simple-word corridor.
GATES_NEW = {
    11: (1_629_748_963_171_204, 2_716_248_271_952_006),
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
    assert 9*(307+k_hi+257+2)//2 < 4000 < OLD_FAR-NEAR
    return r_lo,r_hi,far


def run(*args):
    return subprocess.check_output(list(map(str,args)), text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale',type=int,choices=GATES_NEW,default=11)
    parser.add_argument('--dyadic',type=Path,help='dyadic_survival_758 executable')
    parser.add_argument('--headers',type=Path,help='high_pair_headers_758 executable')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with integer assertions enabled')
    if bool(args.dyadic) != bool(args.headers):
        parser.error('give both verifiers for a complete arithmetic replay')
    r_lo,r_hi,far = physical(args.scale)
    if not args.dyadic:
        print(f'Physical endpoints checked. Denominator exponents {r_lo} through {r_hi}.')
        return

    # At the first grouped depth m>=r the denominator is 4^p, m is r or r+1.
    universal = 23
    lines = run(args.dyadic.resolve(),1,universal,220).splitlines()
    maxima = {}
    for line in lines:
        match = re.search(r'p=(\d+) max=(\d+).*censored=(\d+)',line)
        if match:
            p,maximum,censored = map(int,match.groups())
            assert p not in maxima and censored==0
            maxima[p] = maximum
    assert set(maxima)==set(range(1,universal+1))
    assert max(maxima.values())==187

    for r in range(r_lo,r_hi+1):
        last_guard = 257 if r<=53 else 250
        assert r+1+max(maxima.values()) <= last_guard
        near = GATES_NEW[args.scale][0]
        if r <= 53:
            # Larger distances at the next launch length have a separate budget.
            near = min(near,GATES_NEW[11][0])
        assert horizon(near-2) >= last_guard
        records = []
        for line in run(args.headers.resolve(),r,r,universal+1,last_guard).splitlines():
            values = line.split()
            if len(values)==7 and all(s.isdecimal() for s in values):
                records.append(tuple(map(int,values)))
        assert [row[:2] for row in records] == [(r,p) for p in range(universal+1,(r+1)//2+1)]
        assert records and all(row[-1]==0 for row in records)
        print('All aligned headers return at exponent',r,flush=True)
    print(f'All {far-NEAR+1:,} reset starts with {NEAR:,} <= H-s <= {far:,} halt.')


if __name__ == '__main__':
    main()
