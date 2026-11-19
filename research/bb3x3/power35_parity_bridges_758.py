"""Verify five absorbing parity intervals on the power-35 blank crossing."""
import argparse
from pathlib import Path
from functools import cache

from annular_skip_758 import evaluate, openings

from check_bb33 import first_return
from double35_frontier_758 import CUTS, TABLE, WIDTH, read_table
from power35_inner_skip_758 import certify_word
from power_gates_758 import coalesce


# Start and end grid indices, absorbing parity, last seed of that parity
# with this word, return word after launch, upper bound on the seed gain.
BRIDGES = (
    (1686, 1700, 0, 58_531_956_502_933_810, 'LLJJJLLLLL', 112),
    (1701, 1782, 1, 58_943_610_593_380_613, 'LLLLJLLL', 106),
    (1795, 1800, 1, 59_032_949_563_965_873, 'LLLLJLLJLLLLL', 126),
    (1807, 1883, 0, 59_450_686_841_354_098, 'LLJJJL', 94),
    (1894, 1904, 1, 59_551_950_383_011_749, 'LLLLJLLJJL', 110),
)
# All exits across these three sharp physical boundaries meet exactly.
MERGERS = {
    1701: (58_943_610_593_404_820, 508),
    1795: (59_032_949_564_004_206, 745),
    1807: (59_450_686_841_407_190, 758),
}


# Exact minima and maxima over every one of the 5,001 incoming seeds.
LENGTHS = {
    1701: (4_088_827_510_217, 4_088_827_510_274),
    1795: (228_847_291_387, 228_847_291_435),
    1807: (4_236_857_452_209, 4_236_857_452_267),
}


def count_returns(a, parity, last, word, modulus, merger):
    origin = a + (parity-a)%2
    launch = openings(origin)
    @cache
    def charge(residue):
        x = origin+residue
        return evaluate((launch,word),x)-x

    tails = {merger: 0}
    def tail(x):
        path = []
        while x not in tails:
            assert x < merger
            path.append(x)
            nxt = first_return(x)
            assert nxt is not None and nxt > x
            x = nxt
        length = tails[x]
        for y in reversed(path):
            length += 1
            tails[y] = length
        return length

    def length(seed):
        x, n = (seed, 0) if seed%2 == parity else (first_return(seed), 1)
        seen = {}
        while x <= last:
            residue = (x-origin) % modulus
            if residue in seen:
                old, count = seen[residue]
                stride = x-old
                assert stride > 0 and stride%modulus == 0
                copies = (last-x)//stride
                x += copies*stride
                n += copies*(n-count)
                seen.clear()
            seen[residue] = x, n
            x += charge(residue)
            n += 1
        return n+tail(x)

    lengths = [length(s) for s in range(a,a+WIDTH+1)]
    return min(lengths), max(lengths)


def check_bridge(entry, leave, parity, last, word, gain, with_counts):
    a, b = CUTS[entry], CUTS[leave]
    starts = set()
    for seed in range(a, a + WIDTH + 1):
        if seed % 2 == parity:
            starts.add(seed)
        else:
            nxt = first_return(seed)
            assert nxt is not None and nxt > seed and nxt % 2 == parity
            starts.add(nxt)
    origin = min(starts)
    assert max(starts) < b and b <= last
    modulus = certify_word(origin, last, word)
    # Each J increases a+2c by 4 and every L by at most 9. The
    # ordinary final return adds 5. The initial even move adds 8.
    k = 35 if parity else 34
    assert gain == (8*(1-parity) + 4*(k+word.count('J')) + 9*word.count('L') + 5)//2
    assert gain <= WIDTH and gain % 2 == 0
    # Every trajectory therefore first exits the grid segment in [b,b+WIDTH].
    # At the sharp boundary, only the final 'gain' possible sources can cross.
    cut = last + 1
    exits = {first_return(s) for s in range(cut-gain+(parity-cut+gain)%2, cut, 2)}
    assert None not in exits
    exits = {s for s in exits if s >= cut}
    assert exits and all(s < cut+gain and s%2 == parity for s in exits)
    merger = MERGERS.get(entry)
    if merger:
        assert coalesce(exits,merger[1]) == merger
        if with_counts:
            assert count_returns(a,parity,last,word,modulus,merger[0]) == LENGTHS[entry]
    return merger


def connected(rows, bridges):
    """Every edge accepts any reset in the same grid strip of WIDTH+1 seeds."""
    reached = {0}
    for i in range(len(CUTS)-1):
        if i not in reached:
            continue
        if i in rows:
            reached.add(i+1)
        if i in bridges:
            reached.add(bridges[i])
    return reached


def verify(table, with_counts=False):
    rows = read_table(table)
    edges = {}
    for args in BRIDGES:
        i, j = args[:2]
        merger = check_bridge(*args, with_counts)
        edges[i] = j
        if merger:
            print(f'Grid {i}..{j}, sharp boundary forces reset {merger[0]:,}.')
    reached = connected(rows,edges)
    end = max(reached)
    print(f'The blank orbit reaches grid cut {end} at {CUTS[end]:,}.')
    return rows, reached


def verify_clock(reached):
    from fifth_blank_clock_758 import timed_extension
    assert 1807 in reached
    previous_seed = 58_368_402_051_516_870
    previous_clock = (
        2_477_790_953_640_438_929_769_820_556_786_530_600_455_578_299_331,
        3_639_728_450_719_573_764_610_694_526_768_196_962_921_809_997_952,
    )
    target = MERGERS[1807][0]
    clock = timed_extension(previous_seed,target,[(previous_seed,CUTS[1883],2*10**12)],previous_clock)
    assert clock == (
        2_638_850_660_075_778_516_888_220_150_868_284_148_565_289_781_271,
        3_951_233_789_304_834_198_184_672_340_620_265_502_586_285_652_949,
    )
    print(f'Blank clock at {target:,} in [{clock[0]:,}, {clock[1]:,}].')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table',type=Path,default=TABLE)
    parser.add_argument('--counts',action='store_true',help='verify exact min/max return counts across the three merging intervals')
    parser.add_argument('--clock',action='store_true',help='verify the clock of the exact row-1807 corridor merger')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    _, reached = verify(args.table, args.counts)
    if args.clock:
        verify_clock(reached)
