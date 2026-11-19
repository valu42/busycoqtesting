"""Reproduce outward gates, compressed #758 first returns and the connected checkpoint."""
import argparse
from functools import lru_cache
import heapq
from pathlib import Path

from check_bb33 import champion_step, first_return
from power_approach_758 import EXPONENT as M, POWER as P
from power_cusp_758 import BITS, TABLE, FACTOR, partition
from power_gates_758 import coarse_return


MANIFEST = Path(__file__).with_name('power_ladder_758.tsv')


def pure_interval(k):
    """Offsets d=2i for which J^292 is followed by exactly L^k R."""
    assert k%2 == 1
    a = 2*P-1

    @lru_cache(maxsize=1024)
    def flow(i):
        c = 2*i+2*M+1
        y,gain = (c+7)//2,0
        for _ in range(k//BITS):
            high,low = divmod(y,1<<BITS)
            small,g = TABLE[low]
            y,gain = high*FACTOR+small,gain+g
        for _ in range(k%BITS):
            gain += 5+4*(y%2)
            y = 3*((y+1)//2)
        out = 2*y-7
        return 2*(out-c)-gain,out

    def first(test):
        low, high = 0,P//100
        while low < high:
            mid = (low+high)//2
            if test(*flow(mid)):
                high = mid
            else:
                low = mid+1
        return 2*low

    low = first(lambda decrease,c: decrease+c >= a)
    high = first(lambda decrease,c: decrease > a)
    assert 0 < low < high < P//100
    # The even start word throughout [low,high) is I J^(m-1) LLJLLL R.
    for d in (low+1,high-1):
        assert coarse_return(M,P+d,1) == first_return(P+d)
    return low,high


def fast_return(seed):
    """Exact local return after the known power launch, packing 12 consecutive bulks."""
    assert P <= seed <= 101*P//100
    if seed%2:
        a,c = 2*P-1,seed-P+2*M+1
    else:
        a,c = 4*(P//3)-1,seed-2*(P//3)+2*M+3
    assert c > 0
    while True:
        if a > c:
            while True:
                y = (c+7)//2
                high,low = divmod(y,1<<BITS)
                small,gain = TABLE[low]
                nc = 2*(high*FACTOR+small)-7
                na = a+2*(c-nc)+gain
                # Each intermediate bulk strictly decreases a. This test also
                # excludes an internal first return and checks all the guards.
                if na <= 1:
                    break
                a,c = na,nc
        state = champion_step(a,c)
        if state is None:
            return None
        a,c = state
        if a == 1:
            return c


def merger(edge, width, budget):
    heap = list(range(edge,edge+width))
    live = set(heap)
    heapq.heapify(heap)
    steps = 0
    while len(live) > 1:
        assert steps < budget
        seed = heapq.heappop(heap)
        live.remove(seed)
        result = fast_return(seed)
        if steps < 5 or steps%8191 == 0:
            assert result == first_return(seed)
        assert result is not None and result > seed
        if result not in live:
            heapq.heappush(heap,result)
            live.add(result)
        steps += 1
    return heap[0],steps


def gate(k):
    low,high = pure_interval(k)
    bound = max(620,(4*M+9*k+5)//2)
    checkpoint,edges = merger(P+high,bound,1_000_000)
    return k,low,high,bound,checkpoint-P-high,edges


def check_seam():
    cutoff = P-2*M-4-34*(4*M+40)
    prior = [first_return(s)-s for s in range(cutoff+1,P)]
    assert len(prior) == 41_659 and min(prior)>0 and max(prior)==3409
    q,cells = partition(M,2_000_000,32,0)
    hard=ordinary_cap=hard_cap=0
    for lo,hi,word in cells:
        if word is None:
            for i in range(lo,hi+1):
                seed = P+2*i
                result = first_return(seed)
                assert result is not None and result > seed
                hard_cap = max(hard_cap,result-seed)
                hard += 1
        else:
            cost = 4*M+9*(2*q+word.count('L'))+4*word.count('J')+5
            ordinary_cap = max(ordinary_cap,cost//2)
    assert (len(cells),hard,hard_cap,ordinary_cap) == (39_316,974,3535,4201)
    root,n = merger(P+4_000_001,4500,40_000)
    assert (root-P,n) == (7_627_069,26_388)
    print('all reset phases in the seam reach P+7,627,069')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--k',type=int)
    group.add_argument('--all',action='store_true')
    group.add_argument('--seam',action='store_true')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if args.seam:
        check_seam()
    else:
        rows = [tuple(map(int,line.split())) for line in MANIFEST.read_text().splitlines()
                if line and not line.startswith('#')]
        chosen = rows if args.all else [r for r in rows if r[0] == (args.k or 201)]
        assert chosen
        for row in chosen:
            assert gate(row[0]) == row
        print(f'verified {len(chosen)} outward checkpoints')
