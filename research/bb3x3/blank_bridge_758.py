#!/usr/bin/env python3
"""Check the newly joined blank prefix toward 3^36.

The default checks the receipt chain and replays the exact terminal merger.
Use --worker PATH --replay to recompute the seven new crossing receipts.
Earlier receipts retain their existing verification dependencies.
"""
import argparse
import heapq
from pathlib import Path

from check_bb33 import first_return
import power36_followon_758 as bridge


RECEIPTS = Path(__file__).with_name('blank_bridge_receipts_758.tsv')
INDICES = (28, 30, 31, 32, 33, 34, 51)
LAST_CUT = 52
EXPECTED = 100_583_090_198_237_340


def load_rows(path):
    with path.open() as stream:
        assert next(stream).strip() == 'index '+bridge.HEADER
        rows = {}
        for line in stream:
            index, *values = map(int, line.split())
            assert index not in rows
            rows[index] = bridge.check_row(tuple(values))
            assert rows[index][:2] == tuple(bridge.CUTS[index:index+2])
    return rows


def merger(cut):
    """Reconstruct the common state using only literal first returns."""
    def normalize(seed):
        return seed if seed % 2 == 0 else seed+75+(seed & 2)

    live = {normalize(seed) for seed in range(cut, cut+bridge.WIDTH+1)}
    heap = list(live)
    heapq.heapify(heap)
    edges = 0
    while len(live) > 1:
        assert edges < 25_000
        seed = heapq.heappop(heap)
        live.remove(seed)
        successor = first_return(seed)
        assert successor is not None and seed < successor < bridge.GATE
        successor = normalize(successor)
        if successor not in live:
            live.add(successor)
            heapq.heappush(heap, successor)
        edges += 1
    return heap[0], edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with Python assertions enabled')
    if args.replay and not args.worker:
        parser.error('--replay needs --worker')
    bridge.gate()
    old = load_rows(bridge.REGULAR)
    new = load_rows(RECEIPTS)
    assert tuple(new) == INDICES
    assert set(new).isdisjoint(old)
    if args.replay:
        for index, row in new.items():
            assert bridge.compute(args.worker.resolve(), *row[:2]) == row
            print(f'Replayed new window {index}.', flush=True)
    all_rows = old | new
    # Window zero is the chain of the six previously verified initial cuts.
    with bridge.INITIAL.open() as stream:
        assert next(stream).strip() == bridge.HEADER
        initial = [bridge.check_row(tuple(map(int, line.split()))) for line in stream]
    assert [row[:2] for row in initial] == list(zip(bridge.PREFIX, bridge.PREFIX[1:]))
    for index in range(1, LAST_CUT):
        low, high = bridge.CUTS[index:index+2]
        assert index in all_rows or bridge.simple(low, high), index
    target, edges = merger(bridge.CUTS[LAST_CUT])
    assert (target, edges) == (EXPECTED, 3688)
    certified = {0, *all_rows}
    certified.update(i for i, (lo, hi) in enumerate(zip(bridge.CUTS, bridge.CUTS[1:]))
                     if bridge.simple(lo, hi))
    frontier = next(i for i in range(len(bridge.CUTS)-1) if i not in certified)
    assert frontier == LAST_CUT
    assert len(certified) == 4129
    print(f'From the established blank reset {bridge.START:,}, all windows through {LAST_CUT-1} connect.')
    print(f'The full strip at {bridge.CUTS[LAST_CUT]:,} merges to A(1, {target:,}) in {edges:,} normalized edges.')
    print(f'{len(certified):,} of {len(bridge.CUTS)-1:,} regular windows certified; 702 remain open.')
    print('This finite continuation does not decide the blank-tape halting question.')


if __name__ == '__main__':
    main()
