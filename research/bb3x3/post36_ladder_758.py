#!/usr/bin/env python3
"""Replay singleton connections and exact outward gates above the power-36 reset.

The gate construction accepts any sufficiently large exponent. The supplied
singleton worker is its explicitly bounded exponent-36 implementation.
"""
import argparse
from functools import lru_cache
from pathlib import Path
import subprocess

from check_bb33 import champion_step, first_return
from power_cusp_758 import BITS, TABLE, FACTOR
from power_gates_758 import coarse_return, coalesce
from power36_final_758 import TARGET as START


M = 36
P = 3**M
TARGET = P+30_097_873_249_779
HERE = Path(__file__).resolve().parent
RECEIPTS = HERE/'post36_ladder_receipts_758.tsv'
HEADER = 'k start goal arrival direct_calls merger_calls joins skipped_width gate_low gate_high cap gate_destination gate_edges'


def pure_interval(m, k):
    """Exact even offsets for the word J^m L^k R, with k positive and odd."""
    assert m >= 20 and k > 0 and k%2
    p = 3**m
    a = 2*p-1

    @lru_cache(maxsize=1024)
    def flow(i):
        c = 2*i+2*m+1
        y, gain = (c+7)//2, 0
        for _ in range(k//BITS):
            high, low = divmod(y,1<<BITS)
            small, charge = TABLE[low]
            y, gain = high*FACTOR+small, gain+charge
        for _ in range(k%BITS):
            gain += 5+4*(y%2)
            y = 3*((y+1)//2)
        out = 2*y-7
        return 2*(out-c)-gain, out

    def first(test):
        lo, hi = 0, p//100
        while lo < hi:
            mid = (lo+hi)//2
            if test(*flow(mid)):
                hi = mid
            else:
                lo = mid+1
        return 2*lo

    low = first(lambda decrease,c: decrease+c >= a)
    high = first(lambda decrease,c: decrease > a)
    assert 0 < low < high < p//100
    # Monotone D_k and D_k+c_k make these the exact two boundaries.
    assert sum(flow(low//2-1)) < a <= sum(flow(low//2))
    assert flow(high//2-1)[0] <= a < flow(high//2)[0]
    # The other input parity has its short fixed word throughout this gate.
    for d in (low+1,high-1):
        assert coarse_return(m,p+d,1) == first_return(p+d)
    return low, high


def gate(m,k):
    """Return low,high,cap,forced offset,edge count for one outward gate."""
    p = 3**m
    low, high = pure_interval(m,k)
    cap = max(2*m+29,(4*m+9*k+5)//2)
    target, edges = coalesce(range(p+high,p+high+cap),100_000)
    return low,high,cap,target-p,edges


def read_rows():
    with RECEIPTS.open() as stream:
        assert next(stream).strip() == HEADER
        rows = [tuple(map(int,line.split())) for line in stream if line.strip()]
    assert [row[0] for row in rows] == [25,21]
    return rows


def audit_worker(worker):
    """Independently replay a complete short adaptive flight with scalar calls."""
    worker = str(Path(worker).resolve())
    subprocess.run([worker,'--audit'],check=True)
    receipt = tuple(map(int,subprocess.check_output(
        [worker,str(START),str(P+10_000_000)],text=True).split()))
    assert receipt[:3] == (START,P+10_000_000,P+10_102_544)
    a,c,returns,calls = 1,START,0,0
    while True:
        state = champion_step(a,c)
        assert state is not None
        a,c = state
        calls += 1
        if a == 1:
            returns += 1
            if c >= receipt[2]:
                break
    assert (c,returns,calls) == (P+10_102_544,41_861,3_528_168)
    print('The short adaptive flight agrees with 41,861 literal first returns '
          'and 3,528,168 scalar counter calls.')


def verify(worker=None, from_blank=False):
    assert __debug__, 'enable assertions'
    if from_blank:
        from power36_final_758 import verify as verify_power36
        assert verify_power36() == START
    current = START-P
    for row in read_rows():
        (k,start,goal,arrival,direct_calls,merger_calls,joins,skipped_width,
         low,high,cap,destination,edges) = row
        assert start == current and goal == low <= arrival < high
        assert min(direct_calls,merger_calls,joins,skipped_width) >= 0
        assert skipped_width <= arrival-start
        assert gate(M,k) == (low,high,cap,destination,edges)
        if worker:
            output = subprocess.check_output(
                [str(Path(worker).resolve()),str(P+start),str(P+goal)],text=True)
            absolute = tuple(map(int,output.split()))
            expected = (P+start,P+goal,P+arrival,direct_calls,merger_calls,joins,skipped_width)
            assert absolute == expected, (absolute,expected)
        current = destination
        print(f'Gate k={k}: actual arrival P+{arrival:,}; '
              f'forced reset P+{current:,}; {joins:,} local-word skips.')
    target = P+current
    assert target == TARGET
    print(f'Connected continuation from A(1, {START:,}) to A(1, {target:,}).')
    if not worker:
        print('The connection uses archived singleton receipts; --worker regenerates them.')
    print('This is finite blank-orbit progress; eventual halting remains open.')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path,help='regenerate the singleton connection receipts')
    parser.add_argument('--audit-worker',type=Path,help='audit this worker with an independent short scalar flight')
    parser.add_argument('--from-blank',action='store_true',help='first validate the inherited power-36 chain')
    parser.add_argument('--gate',type=int,help='display an independent outward gate instead')
    parser.add_argument('--exponent',type=int,default=M,help='exponent for --gate (default36)')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if args.audit_worker:
        audit_worker(args.audit_worker)
    elif args.gate is None:
        verify(args.worker,args.from_blank)
    else:
        print(args.exponent,args.gate,*gate(args.exponent,args.gate))


if __name__ == '__main__':
    main()
