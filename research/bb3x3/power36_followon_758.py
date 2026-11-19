#!/usr/bin/env python3
"""Verify the blank reset chain from twice 3^35 to 3^36."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import heapq
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile

from check_bb33 import first_return
from check_confluence import itinerary
from power_gates_758 import coarse_return, coalesce, gate_exits

START = 100_063_090_198_154_948
GATE = 148_364_731_025_779_389
TARGET = 150_094_635_297_111_153
WIDTH = 5_000
STRIDE = 10**13
CUTS = [*range(START, GATE, STRIDE), GATE]
PREFIX = [START, *(START+10**n for n in range(8, 14))]
INITIAL = Path(__file__).with_name('power36_initial_758.tsv')
REGULAR = Path(__file__).with_name('power36_regular_758.tsv')
MERGERS = Path(__file__).with_name('power36_strip_mergers_758.tsv')
HEADER = 'start end min max blocks calls'


def gate():
    p = 3**35
    assert START == 2*p+155_534
    assert coalesce(gate_exits(35, 2), 1893) == (START, 1893)
    near = 3*p-2*36-4
    # In the power-36 gate both parity words advance by an odd, bounded gain.
    for parity, first, last, cap in ((1, GATE, near, 77),
                                     (0, GATE+1, near+79, 101)):
        for seed in (first, last-(last-parity)%2):
            gain = coarse_return(36, seed, 1)-seed
            assert 0 < gain <= cap and gain%2 == 1
    try:
        coarse_return(36, GATE-1, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError('preceding even seed already has the gate word')
    assert GATE+WIDTH < near-34*(4*36+40)
    assert START >= 2*p and GATE <= 3*p-2*35-6-50_000
    assert coalesce(gate_exits(36, 1), 1455) == (TARGET, 1455)


def simple(a, b):
    # Even inputs first take I, and the selected common return may pass
    # intermediate resets. Odd frontiers reach even after one return.
    assert a+WIDTH+77 < b
    left = itinerary(a+a%2)
    right = itinerary(b-1-(b-1)%2)
    word, charge = left
    return left == right and word.endswith('R') and 'E' not in word and charge//2+77 <= WIDTH


def check_row(row):
    assert len(row) == 6
    a,b,low,high,blocks,calls = row
    assert START <= a < b <= GATE and b <= low <= high <= b+WIDTH
    assert low%2 == high%2 == 0 and min(blocks,calls) >= 0
    return row


def compute(worker, a, b):
    output = subprocess.check_output([worker,str(a),str(b)],text=True)
    row = check_row(tuple(map(int,output.split())))
    assert row[:2] == (a,b)
    return row


def bounded_merger(low, high):
    """A window crossing can succeed even when its exits stay separate."""
    live = set(range(low,high+1,2))
    queue = list(live)
    heapq.heapify(queue)
    for edges in range(25_001):
        if len(live) == 1:
            return queue[0],edges
        if edges == 25_000:
            break
        s = heapq.heappop(queue)
        live.remove(s)
        nxt = first_return(s)
        if nxt is None:
            break
        assert nxt > s
        if nxt not in live:
            live.add(nxt)
            heapq.heappush(queue,nxt)
    return None


def verify_strip_mergers():
    """Replay the positive full-strip mergers using the original counter rules."""
    def even(seed):
        return seed if seed%2 == 0 else seed+75+(seed&2)
    with MERGERS.open() as f:
        assert next(f).strip() == 'index reset even_return_edges'
        rows = [tuple(map(int,line.split())) for line in f]
    assert len(rows) == len({i for i,_,_ in rows}) == 475
    assert sum(i < 128 for i,_,_ in rows) == 63
    for i,target,edges in rows:
        assert 0 <= i < len(CUTS) and CUTS[i]+WIDTH < GATE
        live = {even(s) for s in range(CUTS[i],CUTS[i]+WIDTH+1)}
        queue = list(live)
        heapq.heapify(queue)
        for _ in range(edges):
            assert len(live)>1
            s = heapq.heappop(queue)
            live.remove(s)
            nxt = first_return(s)
            assert nxt is not None and s < nxt < GATE
            nxt = even(nxt)
            if nxt not in live:
                live.add(nxt)
                heapq.heappush(queue,nxt)
        assert live == {target}
    print(f'{len(rows)} complete 5,001-seed strips merge through {max(e for _,_,e in rows):,} or fewer normalized edges each.')


def checkpoint_clock():
    """Extend the raw clock across the two certified intervals."""
    from fifth_blank_clock_758 import timed_extension
    from crossing_clock_758 import REACH

    incoming = (
        11_712_678_510_935_380_362_058_354_962_364_020_304_705_317_061_556,
        15_174_090_093_546_359_518_174_460_234_028_779_946_439_652_299_731,
    )
    assert REACH == 100_000
    gate_cut = 3**36-2*36-4
    bounds = timed_extension(START, TARGET, [
        (START, GATE, 2*10**12),
        (GATE, gate_cut, 2*10**12),
    ], incoming)
    assert bounds == (
        39_789_634_331_496_107_883_182_571_926_656_624_298_968_004_896_065,
        51_085_765_306_603_626_485_072_481_483_925_891_912_873_045_730_911,
    )
    for machine, offset in ((758, 0), (153, 50_707)):
        print(f'#{machine} blank clock in [{bounds[0]-offset:,}, {bounds[1]-offset:,}].')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clock',action='store_true',help='check the blank clock after verifying all windows')
    parser.add_argument('--worker',type=Path,help='compiled exponent-35 even-power verifier')
    parser.add_argument('--replay',action='store_true',help='rerun every supplied receipt')
    parser.add_argument('--rows',type=Path,help='directory of additional numbered window receipts')
    parser.add_argument('--strip-mergers',action='store_true',help='replay the 475 whole-strip mergers independently')
    parser.add_argument('--checkpoints',action='store_true',help='merge the exits of every reached archived crossing')
    parser.add_argument('--fill',action='store_true',help='compute missing non-symbolic windows in the selected range')
    parser.add_argument('--jobs',type=int,default=1,help='number of window workers for --fill')
    parser.add_argument('--export',type=Path,help='write a combined regular receipt table atomically')
    parser.add_argument('--require-complete',action='store_true',help='exit unsuccessfully if any regular window is open')
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--stop',type=int,default=len(CUTS)-1,help='exclusive regular-grid index')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1 or not (0 <= args.start <= args.stop < len(CUTS)):
        parser.error('enable assertions and supply valid grid indices')
    if (args.replay or args.fill) and not args.worker:
        parser.error('replay and fill require --worker')
    if args.fill and not args.rows:
        parser.error('fill requires a directory in --rows')
    worker = args.worker.resolve() if args.worker else None
    gate()
    if args.strip_mergers:
        verify_strip_mergers()
    with INITIAL.open() as f:
        assert next(f).strip() == HEADER
        initial = [check_row(tuple(map(int,line.split()))) for line in f]
    assert [row[:2] for row in initial] == list(zip(PREFIX,PREFIX[1:]))
    assert initial[3][2:4] == (100_063_190_198_155_040,)*2
    low,high = initial[-1][2:4]
    assert coalesce(range(low,high+1,2),2728) == (100_073_090_198_235_044,2728)
    if args.replay:
        assert all(compute(worker,*row[:2]) == row for row in initial)
    # The first regular window is the concatenation of the six prefix receipts.
    certified = {i for i,(a,b) in enumerate(zip(CUTS,CUTS[1:])) if simple(a,b)}
    assert len(CUTS)-1 == 4831 and len(certified) == 4095 and 0 not in certified
    certified.add(0)
    regular = {}
    with REGULAR.open() as f:
        assert next(f).strip() == 'index '+HEADER
        for line in f:
            i,*values = map(int,line.split())
            assert i not in regular
            regular[i] = check_row(tuple(values))
    if args.rows:
        if args.fill:
            args.rows.mkdir(parents=True,exist_ok=True)
        for path in args.rows.glob('*.txt'):
            i = int(path.stem)
            row = check_row(tuple(map(int,path.read_text().split())))
            assert regular.setdefault(i,row) == row
    for i,row in regular.items():
        assert 0 <= i < len(CUTS)-1 and row[:2] == tuple(CUTS[i:i+2])
        if args.replay and args.start <= i < args.stop:
            assert compute(worker,*row[:2]) == row
        certified.add(i)
    failures = []
    if args.fill:
        def fill_one(i):
            row = compute(worker,*CUTS[i:i+2])
            # Persist in the completing worker. A slow earlier row cannot
            # delay the durable receipt for an independent later window.
            path = args.rows/f'{i:05}.txt'
            with NamedTemporaryFile(mode='w',dir=args.rows,delete=False) as tmp:
                print(*row,file=tmp)
            Path(tmp.name).replace(path)
            return row
        selected = [i for i in range(args.start,args.stop) if i not in certified]
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(fill_one,i):i for i in selected}
            for future in as_completed(futures):
                i = futures[future]
                try:
                    regular[i] = future.result()
                except (OSError,RuntimeError,subprocess.CalledProcessError) as exc:
                    print(f'Window {i} failed: {exc}',flush=True)
                    failures.append(i)
                else:
                    certified.add(i)
    if args.export:
        with NamedTemporaryFile(mode='w',dir=args.export.parent,delete=False) as tmp:
            print('index '+HEADER,file=tmp)
            for i,row in sorted(regular.items()):
                print(i,*row,file=tmp)
        Path(tmp.name).replace(args.export)
    frontier = next((i for i in range(len(CUTS)-1) if i not in certified),len(CUTS)-1)
    print(f'From the doubled power-35 blank reset {START:,}, the chain reaches cut {CUTS[frontier]:,}.')
    print(f'{len(certified):,} of {len(CUTS)-1:,} regular windows certified, {len(CUTS)-1-len(certified):,} open.')
    if args.checkpoints:
        reached = {row[1]:row[2:4] for row in initial if args.start == 0}
        for i,row in sorted(regular.items()):
            if args.start <= i < min(args.stop,frontier):
                reached[row[1]] = row[2:4]
        with MERGERS.open() as f:
            next(f)
            full_strip = {CUTS[i]:(seed,edges) for i,seed,edges in
                          (map(int,line.split()) for line in f)
                          if args.start < i <= min(args.stop,frontier)}
        for cut in sorted(reached.keys() | full_strip.keys()):
            found = bounded_merger(*reached[cut]) if cut in reached else None
            if found:
                seed,edges = found
                print(f'After cut {cut:,}: exact reset {seed:,} ({edges:,} distinct return edges).')
            elif cut in full_strip:
                seed,edges = full_strip[cut]
                print(f'After cut {cut:,}: full-strip merger at {seed:,} ({edges:,} normalized edges).')
    if frontier == len(CUTS)-1:
        print(f'Both blank runs reach the exact reset {TARGET:,}.')
        if args.clock:
            checkpoint_clock()
    if failures:
        raise SystemExit(f'Uncertified regular windows: {sorted(failures)}')
    if (args.require_complete or args.clock) and frontier != len(CUTS)-1:
        raise SystemExit(f'First missing regular window is {frontier}.')


if __name__ == '__main__':
    main()
