#!/usr/bin/env python3
"""Check the complete blank-to-power-36 window chain and its exact merger.

Without --worker, validate the archived proof chain and replay the gate
merger. Supplying the unchanged exponent-35 worker additionally regenerates
all 584 final crossing receipts.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import power36_followon_758 as bridge
from blank_bridge_758 import RECEIPTS as FIRST_EXTENSION, load_rows


HERE = Path(__file__).resolve().parent
SECOND_EXTENSION = HERE/'power36_complete_receipts_758.tsv'
RECEIPTS = HERE/'power36_final_receipts_758.tsv'
START = bridge.START
GATE = bridge.GATE
TARGET = bridge.TARGET


def verify(worker=None, jobs=1):
    """Return the proved exact reset TARGET after checking complete coverage."""
    assert __debug__, 'run with Python assertions enabled'
    assert jobs >= 1
    archives = [load_rows(path) for path in
                (bridge.REGULAR, FIRST_EXTENSION, SECOND_EXTENSION, RECEIPTS)]
    assert len(archives[-1]) == 584, 'the final receipt archive is incomplete'
    assert all(623 <= index < len(bridge.CUTS)-1 for index in archives[-1])
    all_rows = {}
    for archive in archives:
        assert set(all_rows).isdisjoint(archive), 'overlapping receipt archives'
        all_rows.update(archive)
    if worker:
        worker = Path(worker).resolve()
        def replay(item):
            index, row = item
            assert bridge.compute(worker, *row[:2]) == row, index
            return index
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            for index in pool.map(replay, archives[-1].items()):
                print(f'Replayed final window {index}.', flush=True)

    with bridge.INITIAL.open() as stream:
        assert next(stream).strip() == bridge.HEADER
        initial = [bridge.check_row(tuple(map(int, line.split()))) for line in stream]
    assert [row[:2] for row in initial] == list(zip(bridge.PREFIX, bridge.PREFIX[1:]))
    symbolic = {i for i, (low, high) in enumerate(zip(bridge.CUTS, bridge.CUTS[1:]))
                if bridge.simple(low, high)}
    assert len(symbolic) == 4095
    certified = {0, *all_rows, *symbolic}
    assert certified == set(range(len(bridge.CUTS)-1)), 'a window is still unproved'

    # This rechecks both parity words from the incoming gate strip, their
    # positive bounded gains, and the complete power-36 exit merger.
    bridge.gate()
    assert bridge.CUTS[-1] == GATE
    assert TARGET == 3**36+112_032
    print(f'All {len(certified):,} regular windows connect from the established blank reset {START:,}.')
    print(f'The complete chain enters the strip at {GATE:,} and reaches A(1, {TARGET:,}).')
    print(f'Final archive: {sum(row[-2] for row in archives[-1].values()):,} symbolic blocks and '
          f'{sum(row[-1] for row in archives[-1].values()):,} normalized first-return evaluations.')
    print('Both blank runs reach the power-36 checkpoint; their eventual halting remains open.')
    return TARGET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path, help='regenerate the final 584 receipts with this worker')
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive worker count')
    verify(args.worker, args.jobs)


if __name__ == '__main__':
    main()
