"""Replay the blank-connected bulk corridors just above the doubled power."""
import argparse
from collections import deque
from functools import cache
from typing import NamedTuple

from bulk_digit_cycles_758 import flags
from check_bb33 import champion_step, first_return
from check_confluence import itinerary
from fifth_blank_clock_758 import timed_extension
from power36_followon_758 import (CUTS, GATE, HEADER, INITIAL, PREFIX, REGULAR, START,
                                  TARGET, WIDTH, check_row, gate, simple)
from power_gates_758 import coarse_return, coalesce
from target_clock_758 import first_pass, follow, timed_return


class Corridor(NamedTuple):
    cut: int
    bulks: int
    last_even: int
    destination: int
    exit_count: int
    merger_edges: int
    counts: tuple[int, int, int]
    clock: tuple[int, int]
    cycle: tuple[int, int, int, int]


CORRIDORS = (
    Corridor(35, 13, 100_579_892_930_498_732, 100_579_892_930_565_916, 35, 1240,
             (2, 1_700_198_749_078, 1_700_198_749_129),
             (11_838_458_173_511_211_482_968_407_317_939_796_133_592_905_661_006,
              15_477_415_402_902_052_567_966_318_480_033_313_646_404_995_083_394),
             (167,32_768,19_110,5_090_415_415)),
    Corridor(78, 11, 101_233_452_157_379_468, 101_233_452_157_436_950, 27, 926,
             (3, 3_399_147_919_854, 3_399_147_919_899),
             (12_029_516_641_463_799_224_113_870_091_644_714_792_019_914_097_366,
              15_834_990_276_561_360_219_217_857_645_920_693_681_411_362_894_480),
             (107,12_288,5_514,31_767_737_566)),
    Corridor(2464, 3, 142_194_917_649_788_560, 142_194_917_649_902_128, 17, 1295,
             (11, 198_770_766_496_212, 198_770_766_496_274),
             (33_075_530_690_273_368_308_959_122_852_908_348_472_618_858_341_813,
              40_933_552_599_109_424_964_271_665_809_437_157_342_161_918_067_425),
             (2,176,174,99_385_383_247_888)),
)
PREVIOUS_CLOCK = (
    11_712_678_510_935_380_362_058_354_962_364_020_304_705_317_061_556,
    15_174_090_093_546_359_518_174_460_234_028_779_946_439_652_299_731,
)


def connected(cut):
    # The six initial crossings compose row zero. The subsequent windows may
    # be closed either by identical endpoint words or by worker receipts.
    with INITIAL.open() as receipt:
        assert next(receipt).strip() == HEADER
        rows = [check_row(tuple(map(int, line.split()))) for line in receipt]
        assert [r[:2] for r in rows] == list(zip(PREFIX, PREFIX[1:]))
    with REGULAR.open() as receipt:
        assert next(receipt).strip() == 'index '+HEADER
        seen = set()
        for line in receipt:
            i, *row = map(int, line.split())
            assert check_row(tuple(row))[:2] == tuple(CUTS[i:i+2]) and i not in seen
            seen.add(i)
    assert PREFIX[0] == START and PREFIX[-1] == CUTS[1]
    assert all(i in seen or simple(*CUTS[i:i+2]) for i in range(1, cut))


def normalize(seed):
    return seed if seed % 2 == 0 else seed+75+(seed & 2)


def verify_word(row):
    entry = CUTS[row.cut]
    last = row.last_even
    charge = 8 + 35*4 + 9*row.bulks + 5
    max_gain = charge//2
    cap = max_gain + 77*(max_gain % 2)
    # At the endpoints a is nonincreasing and c nondecreasing with the seed.
    # Each common bulk or jump therefore supplies its guard on every even seed
    # in between. Check for a possible intermediate reset using the smaller a.
    word = 'J'*35 + 'L'*row.bulks
    left = champion_step(1, entry)
    right = champion_step(1, last)
    for letter in word:
        assert left[0] >= right[0] > 1 and left[1] <= right[1]
        for a, c in (left, right):
            if letter == 'L':
                assert a >= 4*((c+1)//4)+3
            else:
                assert a % 2 and a <= c
        left, right = champion_step(*left), champion_step(*right)
    for a, c in (left, right):
        assert a % 2 == 0 and a <= c
    assert itinerary(entry) == itinerary(last) == (word+'R',charge)
    assert itinerary(last+2) != (word+'R',charge)
    assert START <= entry and last+cap < 3**36-2*35-6
    for seed in (entry+1, entry+3, last+cap+1, last+cap+3):
        assert coarse_return(35, seed, 2) == normalize(seed)
    # All bulk mass gains are congruent modulo four, fixing first-return
    # parity. Odd successors normalize with one more return of gain 75 or 77.
    exits = set()
    for seed in range(last-cap, last+1, 2):
        nxt = first_return(seed)
        assert nxt % 2 == max_gain % 2 and 0 < nxt-seed <= max_gain
        even = normalize(nxt)
        if nxt % 2:
            assert even == first_return(nxt)
        if even > last:
            exits.add(even)
    assert len(exits) == row.exit_count
    assert coalesce(exits,row.merger_edges) == (row.destination,row.merger_edges)
    return exits


def counts(row, exits):
    entry = CUTS[row.cut]
    last = row.last_even
    # Each bulk consumes one bit of precision from a right counter known
    # modulo four. This modulus also preserves any odd-to-even normalization.
    modulus = 1 << (row.bulks+1)
    returns_per_edge = 1 + first_return(entry) % 2
    @cache
    def displacement(residue, level):
        if level == 0:
            seed = entry+residue
            nxt = first_return(seed)
            assert 1 + nxt % 2 == returns_per_edge
            gain = normalize(nxt)-seed
            far = seed+((last-seed)//modulus)*modulus
            actual = far
            for _ in range(returns_per_edge):
                actual = first_return(actual)
            assert actual == far+gain
            return gain
        first = displacement(residue, level-1)
        return first+displacement((residue+first) % modulus, level-1)

    tails = {row.destination:(0,0)}
    lengths = []
    actual_exits = set()
    levels = (last-entry+1).bit_length()
    for initial in range(entry, entry+WIDTH+1):
        seed = normalize(initial)
        if initial % 2:
            assert first_return(initial) == seed
        steps = initial % 2
        for level in reversed(range(levels)):
            gain = displacement((seed-entry) % modulus, level)
            if seed+gain <= last:
                seed += gain
                steps += returns_per_edge * (1 << level)
        seed += displacement((seed-entry) % modulus,0)
        assert seed in exits
        actual_exits.add(seed)
        tail, _ = follow(seed,tails,row.destination)
        lengths.append(steps+returns_per_edge+tail)
    return len(actual_exits), min(lengths), max(lengths)


def cycle(row):
    """Check every residue phase, its cycle and its lifted displacement."""
    modulus = 1 << row.bulks
    entry = CUTS[row.cut]
    # After IJ^35, y=(c+7)/2=seed/2-3^35+41. One normalized
    # step changes y by half the seed gain, regardless of its length in returns.
    origin = entry//2 - 3**35 + 41
    gain = []
    parents = [[] for _ in range(modulus)]
    k = row.bulks//4
    for y in range(modulus):
        bits = flags(y,row.bulks)[1].bit_count()
        if row.bulks % 4 == 3:
            delta = 35+5*k+7+bits
        else:
            delta = 70+5*k+7+bits+((y+k+bits+1) % 2)
        seed = entry+2*((y-origin) % modulus)
        assert normalize(first_return(seed)) == seed+2*delta
        gain.append(delta)
        parents[(y+delta) % modulus].append(y)

    path = {}
    phase = lift = 0
    while phase not in path:
        path[phase] = (len(path),lift)
        lift += gain[phase]
        phase = lift % modulus
    first, old_lift = path[phase]
    members = list(path)[first:]
    seed_stride = 2*(lift-old_lift)
    to_cycle = {y:0 for y in members}
    queue = deque(members)
    while queue:
        current = queue.popleft()
        for y in parents[current]:
            if y not in to_cycle:
                to_cycle[y] = 2*gain[y]+to_cycle[current]
                queue.append(y)
    assert len(to_cycle) == modulus  # There are no other cycles.
    # Allow any odd entrant its short return before starting the even orbit.
    latest_cycle_entry = entry+WIDTH+77+max(to_cycle.values())
    repeats = (row.last_even-latest_cycle_entry)//seed_stride
    return len(members), seed_stride, max(to_cycle.values()), repeats


def three_bulk_clock(row):
    """Time the full passage for each of the 5,001 certified entrances."""
    assert row.bulks == 3
    entry = CUTS[row.cut]
    tails = {row.destination:(0,0)}
    outcomes = []
    for seed in range(entry,entry+WIDTH+1):
        even, prefix = timed_return(seed) if seed % 2 else (seed,0)
        exit_seed, n, flight = first_pass(even,entry,row.last_even,16,90)
        steps, tail = follow(exit_seed,tails,row.destination)
        outcomes.append((prefix+flight+tail,seed,n+steps+seed%2))
    assert (min(t[2] for t in outcomes),max(t[2] for t in outcomes)) == row.counts[1:]
    assert min(outcomes) == (10_008_882_320_792_462_921_809_643_614_479_063_065_790_190_824_028,
                             124_703_090_198_159_929,198_770_766_496_218)
    assert max(outcomes) == (10_008_882_320_795_622_214_370_521_408_577_381_386_855_966_625_542,
                             124_703_090_198_155_006,198_770_766_496_272)
    # The actual entrance lies in [entry,entry+WIDTH]. Lower credits and
    # upper savings stop at entry. The generic upper potential is increasing.
    low, high = timed_extension(START,entry+WIDTH,[(START,entry,2*10**12)],PREVIOUS_CLOCK)
    return low+min(outcomes)[0], high+max(outcomes)[0]


def final_clocks():
    """Extend the tightly timed three-bulk passage through the verified grids."""
    from double36_frontier_758 import CUTS as next_cuts, TABLE as next_table, read_table

    connected(len(CUTS)-1)
    gate()
    row = CORRIDORS[-1]
    intervals = [(row.destination,GATE,2*10**12), (GATE,3**36-76,2*10**12)]
    lower,upper = timed_extension(row.destination,TARGET,intervals,row.clock)
    assert (lower,upper) == (
        40_012_539_094_432_622_425_761_039_078_783_022_163_296_725_878_663,
        50_608_957_723_627_340_180_750_709_167_530_934_478_033_830_181_741,
    )
    print(f'At {TARGET:,}, #758 raw clock [{lower:,}, {upper:,}].')
    rows = read_table(next_table,next_cuts)
    assert next_cuts[0] == TARGET and all(i in rows for i in range(6))
    _,cut,low,high,_,_ = rows[5]
    destination,edges = coalesce(range(low,high+1),858)
    assert (destination,edges) == (150_154_635_297_142_749,858)
    lower,upper = timed_extension(TARGET,destination,[(TARGET,cut,2*10**12)],(lower,upper))
    assert (lower,upper) == (
        40_043_628_698_012_653_507_859_719_075_457_778_414_715_574_797_556,
        50_698_722_796_009_830_424_148_244_736_658_574_776_398_582_497_004,
    )
    print(f'At {destination:,}, #758 raw clock [{lower:,}, {upper:,}].')
    print(f'At {destination:,}, #153 raw clock [{lower-50_707:,}, {upper-50_707:,}].')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clock',action='store_true')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    for row in CORRIDORS:
        connected(row.cut)
        actual, smallest, largest = counts(row, verify_word(row))
        assert (actual, smallest, largest) == row.counts
        entry = CUTS[row.cut]
        period, stride, transient, copies = cycle(row)
        assert (period, stride, transient, copies) == row.cycle
        print(f'Cycle: {period:,} normalized returns, seed stride {stride:,}, '
              f'transient gain at most {transient:,}, at least {copies:,} full copies.')
        print(f'{entry:,}..{entry+WIDTH:,}: {actual} normalized exits, '
              f'{smallest:,}..{largest:,} first returns to {row.destination:,}.')
        if args.clock:
            if row.bulks == 3:
                lower,upper = three_bulk_clock(row)
            else:
                interval = [(START,row.last_even,10**13)]
                lower,upper = timed_extension(START,row.destination,interval,PREVIOUS_CLOCK)
            assert (lower,upper) == row.clock
            print(f'#758 clock [{lower:,}, {upper:,}].')
            print(f'#153 clock [{lower-50_707:,}, {upper-50_707:,}].')
    if args.clock:
        final_clocks()


if __name__ == '__main__':
    main()
