"""Verify that a mass crossing alone forces the named #758/#153 blank checkpoint."""
import argparse
from fractions import Fraction
from functools import cache
from pathlib import Path
import subprocess

from check_bb33 import HALTING_TARGET, champion_step
from power_gates_758 import MANIFEST, coalesce, gate_exits
from three_bulk_scale_transport_758 import TABLE, blank_cut, bulk_end, corridor, exceptional_band, exit_offsets, one_bulk_band


RECEIPTS = Path(__file__).with_suffix('.tsv')
GAINS = (5, 9, 7, 7)
BIASES = (20, 35, 26, 29)


def angular_work(cut):
    """Count every padded leaf and distinct integer d without enumerating the leaves."""
    @cache
    def visit(width, residue, depth):
        if width <= 32*24:
            error = 9*(depth+1)//(14*32)
            low = -7-error
            high = (residue+width+31)//32+4+error
            return 1,high-low+1,low,high,low,high,depth
        left = visit((4*width+8)//9,residue,depth+1)
        offset = 2*width//3
        whole,phase = divmod(residue+offset,32)
        right = visit(width-offset,phase,depth+1)
        nl,cl,first,first_end,last,last_end,dl = left
        nr,cr,start,start_end,end,end_end,dr = right
        start,start_end,end,end_end = (v+whole for v in (start,start_end,end,end_end))
        assert last <= start and last_end <= start_end
        overlap = max(0,last_end-start+1)
        return nl+nr,cl+cr-overlap,first,first_end,end,end_end,max(dl,dr)

    leaves,count,first,_,_,_,depth = visit(16*cut,0,0)
    states = visit.cache_info().currsize
    visit.cache_clear()
    return leaves,count+min(0,first),depth,states


def exact_step(u, d):
    """An actual complete ordinary J or pair; reject intermediate or final resets."""
    a, c = 2*u-4*d-1, 2*d+1
    if a <= 1 or d < 0:
        return None
    if a <= c:
        a, c = champion_step(a,c)
    else:
        for _ in range(2):
            if a <= 1 or a < 4*((c+1)//4)+3:
                return None
            a, c = champion_step(a,c)
    if a <= 1:
        return None
    return (a+2*c-1)//2, (c-1)//2


def scalar_upper(u, d):
    """The C++ future may include a reset; compare each retained ordinary call."""
    count = 0
    while True:
        actual = exact_step(u,d)
        if 3*d+1 >= u:
            new = u+2, 3*d+1-u
        else:
            r = d%4
            up, dp = u+GAINS[r], (9*d+BIASES[r])//4
            if 2*dp >= up:
                assert actual is None
                return count
            new = up,dp
        assert actual is None or actual == new
        u,d = new
        count += 1
        assert count < 512


def physical_crossings(cut):
    """Enumerate genuine 32-call arrivals at a small cut by original forward rules."""
    arrivals = set()
    # An aligned start 32 or 33 calls earlier lies within 149 half-mass units.
    for start in range(cut-150,cut):
        for initial_d in range((start+1)//2):
            u,d,calls = start,initial_d,0
            while u < cut:
                new = exact_step(u,d)
                if new is None:
                    break
                calls += 1 if 3*d+1 >= u else 2
                u,d = new
            else:
                if calls >= 32:
                    arrivals.add((u,d))
    longest = 0
    for u,d in arrivals:
        length = 0
        while (new := exact_step(u,d)) is not None:
            u,d = new
            length += 1
        longest = max(longest,length)
    return len(arrivals),longest


def enclosure(m, cut, length):
    p = 3**m
    a,b = next((a,b) for a,b in ((5,1),(113,20),(92,25)) if exceptional_band(m,a,b,10_000))
    center = Fraction(a*p,b)
    radius = center/10_000
    assert cut == int(center/2)
    nearest = int(center)
    n,live = bulk_end((nearest+(1-nearest)%2+6,1))
    assert live
    # Each grouped block contains at most two calls. The cut can overshoot
    # by eight half-mass units. Extra calls cover both partial end blocks.
    low = 2*cut+1-9*(32+4)
    high = 2*cut+1+16+18*(length+4)
    assert center-radius < low and high+9*(n+2) < center+radius
    if (a,b) == (92,25):
        one_bulk_band(m)
        first = (center-radius-1)/2
        last = (center+radius-1)/2
        gate = (19*p+9)//10
        assert 100*first >= 183*p and last < gate
        assert gate+2*m+9 <= min(195*p//100, 2*p-2*m-6-34*(4*m+40))
        with MANIFEST.open() as src:
            rows = [tuple(map(int,line.split())) for line in list(src)[1:]]
        _,_,_,edges,offs = next(row for row in rows if row[:2] == (m,2))
        checkpoint,steps = coalesce(gate_exits(m,2),edges)
        assert (checkpoint-2*p,steps) == (offs,edges)
    else:
        low_seed,high_seed = corridor(m)
        assert low_seed <= (center-radius-1)/2 <= (center+radius-1)/2 <= high_seed-10*(2*m+20)
        with TABLE.open() as src:
            rows = [tuple(map(int,line.split())) for line in list(src)[1:]]
        _,_,edges,checkpoint = next(row for row in rows if row[0] == m)
        assert coalesce((high_seed+2*j for j in exit_offsets(m)),edges) == (checkpoint,edges)
        blank_cut(m)
    return low,high,checkpoint


def run(binary, cut, brute=False):
    command = [str(binary), *(['--brute'] if brute else []), str(cut)]
    return tuple(map(int,subprocess.check_output(command,text=True).split()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary',type=Path,nargs='?',help='compiled ordinary_band_sieve_758.cpp')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all',action='store_true')
    group.add_argument('--m',type=int,default=20)
    group.add_argument('--count',metavar='CUT',help='count the full angular search at an integer half-mass or at the target cut')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if args.count is not None:
        cut = HALTING_TARGET-10_000_000 if args.count == 'target' else int(args.count)
        if cut < 1:
            parser.error('the cut must be positive')
        leaves,count,depth,states = angular_work(cut)
        print(f'Cut {cut}: {leaves} leaves, {count} integer coordinates, '
              f'maximum depth {depth}, {states} memoized states.')
        return
    if args.binary is None:
        parser.error('specify the compiled verifier or use --count')
    binary = args.binary.resolve(strict=True)
    for small in (10_000,12_345,25_000):
        fast = run(binary,small)
        slow = run(binary,small,brute=True)
        assert fast[-3:] == slow[-3:] and fast[-3] >= fast[-4]
        assert scalar_upper(fast[-2],fast[-1]) == fast[-3]
    assert physical_crossings(10_000) == (34,15)
    with RECEIPTS.open() as src:
        assert next(src).split() == 'm cut leaves scanned presieved replays max_depth future upper_mass arg_d'.split()
        rows = [tuple(map(int,line.split())) for line in src]
    assert [r[0] for r in rows] == list(range(20,20+len(rows)))
    if not args.all and args.m not in range(20,20+len(rows)):
        parser.error('an archived exponent is required')
    for m,*receipt in rows:
        if not args.all and m != args.m:
            continue
        cut = receipt[0]
        assert angular_work(cut)[:3] == (receipt[1],receipt[2],receipt[-4])
        assert run(binary,cut) == tuple(receipt)
        depth,tail,arg_u,arg_d = receipt[-4:]
        assert cut <= arg_u <= cut+8 and scalar_upper(arg_u,arg_d) == tail
        length = max(depth,tail)
        low,high,checkpoint = enclosure(m,cut,length)
        print(f'm={m}: a crossing from W<={low} to W>={high} forces reset {checkpoint}; '
              f'at most {length} ordinary blocks after the middle cut.',flush=True)


if __name__ == '__main__':
    main()
