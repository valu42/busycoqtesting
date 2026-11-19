"""A sufficient next gate above the fifth candidate of BB(3,3) #758."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

from check_confluence import itinerary
from fifth_crossing_758 import K
from power_gates_758 import coarse_return, coalesce, gate_exits

START = K + 118
CUT = 49_454_910_341_926_411
GOAL = 3**35 + 34_754


CUTS = [*range(START, CUT, 10**13), CUT]


def verify_gate():
    m = 35
    power = 3**m
    last_odd = power-2*m-4
    first_even = CUT+1
    for parity, start, last, limit in (
        (0, first_even, last_odd + 2*m+7, 2*m+29),
        (1, START+1, last_odd, 2*m+5),
    ):
        for seed in (start, last-(last-parity)%2):
            assert seed % 2 == parity
            gain = coarse_return(m, seed, 1)-seed
            assert 0 < gain <= limit and gain % 2

    # The preceding even seed changes word; the odd seed CUT is included.
    try:
        coarse_return(m, first_even-2, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError('the lower endpoint is not sharp for even seeds')
    low = (9999*power+9999)//10000
    margin = 34*(4*m+40)
    assert CUT+5_000 < low and low+2*m+29 < last_odd-margin
    exits = gate_exits(m, 1)
    assert len(exits) == 13 and coalesce(exits, 550) == (GOAL, 550)

    # The existing exponent-34 paired worker is sound on the entire gap.
    p = 3**34
    assert 2*p <= START < CUT <= 3*p-2*34-6-50_000
    assert len(CUTS)-1 == 897

    # A concrete target for continuation from GOAL.
    next_cut = 90_056_781_178_199_398
    double_end = 2*power-2*m-6
    for parity, top in enumerate((double_end, double_end+2*m+11)):
        for seed in (next_cut+(parity-next_cut)%2, top-(top-parity)%2):
            assert coarse_return(m,seed,2) > seed
    assert next_cut+5_000 < double_end-34*(4*m+40)
    next_exits = gate_exits(m,2)
    assert len(next_exits) == 39
    assert coalesce(next_exits,1893) == (100_063_090_198_154_948,1893)


def simple_windows():
    # Odd inputs normalize to even after one exact return of gain <=75.
    # Matching ordinary endpoint words certify a selected live reset for
    # every even input up to the next cut. The mass-charge limit remains
    # valid if the selected return has an earlier intermediate reset.
    last_odd = 3**35-2*35-4
    simple = set()
    for i, (a,b) in enumerate(zip(CUTS,CUTS[1:])):
        assert a+5_000+75 < b and b+5_000 < last_odd
        left = itinerary(a+a%2)
        right = itinerary(b-1-(b-1)%2)
        common_word, mass_gain = left
        if (left == right and common_word.endswith('R') and 'E' not in common_word
                and mass_gain//2+75 <= 5_000):
            simple.add(i)
    assert len(simple) == 763
    return simple


def read_receipts(path, simple):
    records = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        i, a, b, low, high, blocks, calls = map(int, line.split())
        assert 0 <= i < len(CUTS)-1 and i not in records and i not in simple
        assert [a,b] == CUTS[i:i+2] and b <= low <= high <= b+5_000
        assert min(blocks,calls) >= 0
        records[i] = (a,b,low,high,blocks,calls)
    return records


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, help='packed-worker supplement to the 763 simple windows')
    parser.add_argument('--worker', type=Path, help='compiled exponent-34 worker, for optional full replay')
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--clock', action='store_true', help='time the reached checkpoint with complete receipts')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1 or (args.worker and not args.receipts):
        parser.error('enable assertions, use positive jobs and supply --receipts for worker replay')
    verify_gate()
    simple = simple_windows()
    records = read_receipts(args.receipts, simple) if args.receipts else {}
    missing = sorted(set(range(len(CUTS)-1))-simple-records.keys())
    if args.worker:
        def replay(row):
            line = subprocess.check_output([args.worker.resolve(),*map(str,row[:2])],text=True)
            assert tuple(map(int,line.split())) == row
        with ThreadPoolExecutor(args.jobs) as pool:
            for _ in pool.map(replay,records.values()):
                pass
    if missing:
        print(f'{len(simple)} simple and {len(records)} packed windows. First uncovered index '
              f'{missing[0]} at cut {CUTS[missing[0]]:,}.')
        if args.require_complete or args.clock:
            raise SystemExit(f'{len(missing)} windows missing')
    else:
        print(f'All 897 windows connect the fifth crossing to 3^35+34,754 = {GOAL:,}.')
    print(f'Entry in {CUT:,}..{CUT+5_000:,} forces a visit to reset {GOAL:,}.')
    if args.clock:
        from fifth_blank_clock_758 import timed_extension, verify
        _, previous = verify()
        cutoff = 3**35 - 2*35 - 4
        intervals = ((START, CUT, 2*10**12), (CUT, cutoff, 2*10**12))
        bounds = timed_extension(START, GOAL, intervals, previous)
        assert bounds == (
            1_482_784_176_152_518_686_967_781_313_684_540_616_202_754_440_890,
            1_988_454_072_317_701_732_753_123_726_748_110_537_604_032_294_736,
        )
        print('Raw clock at the power-35 checkpoint:', *bounds)


if __name__ == '__main__':
    main()
