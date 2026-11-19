"""Check the blank-orbit link from the fourth pair to the doubled power of three."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from pathlib import Path
import subprocess

from after_fourth_758 import CHECKPOINT
from power_gates_758 import coarse_return, coalesce, gate_exits
from survey_next_power_758 import END, STRIDE


MANIFEST = Path(__file__).with_name("double34_crossings_758.tsv.gz")
POWER = 3**34
NEXT = 2*POWER + 32_211


def rows():
    cuts = [*range(CHECKPOINT, END, STRIDE), END]
    with gzip.open(MANIFEST, 'rt') as file:
        assert next(file).split() == ['start', 'end', 'min', 'max', 'blocks', 'calls']
        result = [tuple(map(int, line.split())) for line in file]
    assert len(result) == len(cuts)-1 == 5_820
    for (start, end, low, high, blocks, calls), a, b in zip(result, cuts, cuts[1:]):
        assert (start, end) == (a, b)
        assert end <= low <= high <= end+5_000 and min(blocks, calls) >= 0
    return result


def gate():
    near = 2*POWER - 2*34 - 6
    assert END+5_000 < near-34*(4*34+40)
    for parity, top in enumerate((near,near+2*34+11)):
        first = END+(parity-END)%2
        for seed in (first, top-(top-parity)%2):
            assert coarse_return(34, seed, 2) > seed
    actual = coalesce(gate_exits(34, 2), 693)
    assert actual == (NEXT, 693)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--worker',type=Path,help='compiled cross_758_fast.cpp, to replay the grid')
    p.add_argument('--jobs',type=int,default=1)
    p.add_argument('--start',type=int,default=0,help='first window for optional replay')
    p.add_argument('--stop',type=int,default=5_820,help='exclusive last window for optional replay')
    args = p.parse_args()
    if not __debug__ or not 0 <= args.start <= args.stop <= 5_820 or args.jobs < 1:
        p.error('enable assertions and supply a valid interval and worker count')
    records = rows()
    gate()
    if args.worker:
        exe = args.worker.resolve()
        def replay(row):
            result = subprocess.check_output([exe, str(row[0]), str(row[1])], text=True)
            assert tuple(map(int, result.split())) == row
        with ThreadPoolExecutor(args.jobs) as pool:
            for _ in pool.map(replay, records[args.start:args.stop]):
                pass
    print(f'{len(records):,} consecutive windows connect blank to reset {NEXT:,}.')


if __name__ == '__main__':
    main()
