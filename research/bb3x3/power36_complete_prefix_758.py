#!/usr/bin/env python3
"""Verify the extended connected blank prefix toward the power-36 gate.

Receipt replay uses the unchanged exponent-35 C++ worker. The default checks
the complete connected chain and reconstructs its final exact reset using
literal first returns.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import power36_followon_758 as bridge
from blank_bridge_758 import RECEIPTS as PREVIOUS_RECEIPTS, load_rows, merger


RECEIPTS = Path(__file__).with_name('power36_complete_receipts_758.tsv')
LAST_CUT = 623
EXPECTED = 106_293_090_198_412_080


def verify(worker=None, jobs=1):
    bridge.gate()
    old, previous, new = map(load_rows, (bridge.REGULAR, PREVIOUS_RECEIPTS, RECEIPTS))
    assert len(new) == 118
    assert set(new).isdisjoint(old) and set(new).isdisjoint(previous)
    assert all(52 <= index < 407 or index == 622 for index in new)
    if worker:
        def replay(item):
            index, row = item
            assert bridge.compute(worker.resolve(), *row[:2]) == row, index
            return index
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            for index in pool.map(replay, new.items()):
                print(f'Replayed window {index}.', flush=True)

    with bridge.INITIAL.open() as stream:
        assert next(stream).strip() == bridge.HEADER
        initial = [bridge.check_row(tuple(map(int, line.split()))) for line in stream]
    assert [row[:2] for row in initial] == list(zip(bridge.PREFIX, bridge.PREFIX[1:]))
    all_rows = old | previous | new
    certified = {0, *all_rows}
    certified.update(i for i, (low, high) in enumerate(zip(bridge.CUTS, bridge.CUTS[1:]))
                     if bridge.simple(low, high))
    assert all(index in certified for index in range(LAST_CUT))
    assert LAST_CUT not in certified
    assert len(certified) == 4247
    target, edges = merger(bridge.CUTS[LAST_CUT])
    assert (target, edges) == (EXPECTED, 5384)
    print(f'All windows through {LAST_CUT-1} connect from the established blank prefix.')
    print(f'The cut at {bridge.CUTS[LAST_CUT]:,} merges to A(1, {target:,}) in {edges:,} normalized edges.')
    print(f'{len(certified):,} of {len(bridge.CUTS)-1:,} regular windows certified; 584 remain open.')
    print(f'New receipts: {sum(row[-2] for row in new.values()):,} symbolic blocks and '
          f'{sum(row[-1] for row in new.values()):,} normalized first-return evaluations.')
    print('The power-36 connection and blank-tape halting question remain open.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path, help='recompute new receipts with this exponent-35 worker')
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive worker count')
    verify(args.worker, args.jobs)


if __name__ == '__main__':
    main()
