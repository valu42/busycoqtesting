#!/usr/bin/env python3
"""Replay the scale-10 extension or bound the unknown part of all three inner gaps."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
OLD_FAR = 905_416_090_650_670
BASIN_NEAR = 543_249_654_390_404
DIRECT_SPAN = 250_000


def rows(path):
    return [tuple(map(int, line.split())) for line in path.read_text().splitlines()]


def gap_bounds(path):
    gaps = defaultdict(list)
    for scale, far, near, nodes, calls, halts, count, maxgain, low, high in rows(path):
        if scale < 8:
            continue
        width = far - near + 1
        # Any nonempty full-tree leaf has at least the following integer width.
        assert width > DIRECT_SPAN and (DIRECT_SPAN + 1) // 2 > maxgain
        assert 0 < maxgain <= 5000 and count > 0 and near-5000 <= low <= high < near
        assert nodes % 2 == 1 and calls >= 0 and halts == 0
        # A visited full binary tree has (nodes+1)/2 leaves. Every direct leaf
        # has at most DIRECT_SPAN+1 integer distances. Distinct direct lookups
        # in one row all certify distinct origins.
        leaves = (nodes + 1) // 2
        unknown = 0 if nodes == 1 else leaves * (DIRECT_SPAN + 1) - calls
        assert unknown >= 0
        gaps[scale].append((near, far, unknown))
    for n, records in sorted(gaps.items()):
        records.sort()
        assert all(r[1] == s[0] for r, s in zip(records, records[1:]))
        width = records[-1][1] - records[0][0] + 1
        unknown = sum(r[2] for r in records)
        print(n, width, width-unknown, unknown)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gap-bounds', action='store_true')
    p.add_argument('--worker', type=Path, default=HERE/'gateway_758')
    p.add_argument('--row', type=int)
    p.add_argument('--jobs', type=int, default=1)
    args = p.parse_args()
    if not __debug__ or args.jobs < 1:
        p.error('positive jobs and enabled assertions required')
    if args.gap_bounds:
        gap_bounds(HERE/'lower_scale_bridges_758.tsv')
        return
    data = rows(HERE/'outer_wall_758.tsv')
    assert data and data[0][0] == OLD_FAR
    assert all(a[1] == b[0] for a, b in zip(data, data[1:]))
    for lo, hi, nodes, leaves in data:
        assert OLD_FAR <= lo < hi <= 10**15
        assert nodes == 2*leaves-1 and leaves >= 1
        # Even first-return increments are <=615. The reference checks an odd
        # prefix bound, <=309 jumps, and <10000 additional moves at <=9 gain.
        assert lo - BASIN_NEAR > (4*(293+309)+9*14+9*10000+5)//2
    if args.row is not None and not 1 <= args.row <= len(data):
        p.error('invalid one-based row')
    from check_bb33 import HALTING_TARGET as H
    from lower_clock_758 import lower_at_mass, make_graph, certify_potential
    far = data[-1][1]
    terminal_mass = 2*H+1258
    entry_mass = 2*(H-far)+1
    max_calls = (terminal_mass-entry_mass)//4+1
    cost = (terminal_mass**2+30*terminal_mass+195)//3
    assert max_calls*cost < 2823*10**290
    lower = lower_at_mass(entry_mass, certify_potential(make_graph()))-50707
    assert lower > 210448*10**409
    selected = data if args.row is None else [data[args.row-1]]
    worker = str(args.worker.resolve(strict=True))

    def verify(row):
        lo, hi, _, _ = row
        answer = subprocess.check_output([worker, '--universal', str(hi), str(lo)], text=True)
        if tuple(map(int, answer.split())) != row:
            raise ValueError(f'reference result differs at {lo}..{hi}')
        return lo, hi

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for lo, hi in pool.map(verify, selected):
            print(f'Checked {lo} through {hi}', flush=True)


if __name__ == '__main__':
    main()
