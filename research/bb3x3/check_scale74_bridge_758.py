#!/usr/bin/env python3
"""Verify the first-change obstruction, post-change join and optional full scale-74 cover."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import heapq
from itertools import groupby
from pathlib import Path
import subprocess

from check_bb33 import first_return
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word, cycle_exits, first_change

ORIGIN = 1_865_347_548_659_819_442_523_519_543_121_952_886_355_592_304
LIMIT = 1_000_000_000_000
CHECKPOINT = 1_000_009_062_455
FIRST_WORD = PREFIX + 'J'*191 + 'L'*240 + 'JLLJLR'
HERE = Path(__file__).resolve().parent


def formal_gain(seed, word):
    """Evaluate mass-gain residues for a fixed word, independently of its guards."""
    mask = (1 << (word.count('L')+1)) - 1
    a, c, gain = 1, seed & mask, 0
    for move, group in groupby(word):
        count = sum(1 for _ in group)
        if move == 'I':
            assert count == 1
            a, c, gain = 3, (c+3) & mask, gain+8
        elif move == 'J':
            power = 3**count
            c = (c-(a+1)*((power-1)//2)+2*count) & mask
            a = (power*(a+1)-1) & mask
            gain += 4*count
        elif move == 'L':
            for _ in range(count):
                high = c % 4 == 3
                a = (a-c-(4 if high else 2)) & mask
                mask >>= 1
                c = ((3*c+(13 if high else 7))//2) & mask
                gain += 9 if high else 5
        else:
            assert move == 'R' and count == 1
            return (gain+5)//2
    raise ValueError('word lacks a terminal return')


def check_start():
    assert first_change(74) == ORIGIN
    assert cycle_exits(74, lower=ORIGIN) == ([(64, 1)], [812])
    base = H-ORIGIN
    gains = [check_word(base+z, FIRST_WORD) for z in range(806,817,2)]
    assert gains == [1895, 1893, 1865, 1863, 1863, 1861]
    for z in (804, 818):
        try:
            check_word(base+z, FIRST_WORD)
        except AssertionError:
            continue
        raise AssertionError('claimed edge of word was not sharp')
    seed = base+812
    assert check_word(seed+1863, EVEN_WORD) == 609
    high_bit = 1 << 257
    def pair(s):
        first = formal_gain(s, FIRST_WORD)
        return first, first+formal_gain(s+first, EVEN_WORD)
    assert FIRST_WORD.count('L') == 257
    assert pair(seed) == (1863,2472) and pair(seed+high_bit) == (1865,2476)
    # The even reset word holds throughout this range by the endpoint order.
    for z in (813,LIMIT-1):
        assert 0 < check_word(base+z, EVEN_WORD) <= 615


def join():
    base = H-ORIGIN
    active = set(range(LIMIT+1,LIMIT+2534))
    queue = list(active)
    heapq.heapify(queue)
    edges = 0
    while len(active)>1:
        z = heapq.heappop(queue)
        active.remove(z)
        result = first_return(base+z)
        assert result is not None and result>base+z
        target = result-base
        if target not in active:
            active.add(target)
            heapq.heappush(queue,target)
        edges += 1
    assert active == {CHECKPOINT}
    return edges


def bands():
    rows = [tuple(map(int,line.split())) for line in
            (HERE/'scale74_bridge_758.tsv').read_text().splitlines()]
    expected = [(812,10**9)] + [(a,min(a+10**10,LIMIT))
                                for a in range(10**9,LIMIT,10**10)]
    assert [row[:2] for row in rows] == expected
    assert all(nodes == 2*leaves-1 for lo,hi,nodes,leaves,gain in rows)
    assert max(row[4] for row in rows) == 2533
    assert sum(row[2] for row in rows) == 1_240_135_053
    assert sum(row[3] for row in rows) == 620_067_577
    return rows


def main():
    if not __debug__:
        raise SystemExit('Leave assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--full', action='store_true')
    group.add_argument('--row', type=int)
    parser.add_argument('--checker', type=Path, default=HERE/'scale74_bridge_758')
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()
    rows = bands()
    if args.jobs < 1 or (args.row is not None and not 1<=args.row<=len(rows)):
        parser.error('invalid job count or row number')
    check_start()
    print(f'Exact post-change join at offset {CHECKPOINT:,} via {join():,} first returns.',
          flush=True)
    chosen = rows if args.full else rows[args.row-1:args.row] if args.row else []
    def replay(row):
        lo,hi = row[:2]
        result = subprocess.run([str(args.checker.resolve()),str(lo),str(hi)],
                                capture_output=True,text=True,check=True)
        assert tuple(map(int,result.stdout.split())) == row
        return lo,hi
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for lo,hi in pool.map(replay,chosen):
            print(f'Checked offsets {lo} through {hi}.', flush=True)


if __name__ == '__main__':
    main()
