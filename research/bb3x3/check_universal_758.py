#!/usr/bin/env python3
"""Replay contiguous #758 wall certificates with the exact GMP gateway checker."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def bands(end):
    """This partition fixes the comparable nodes and leaves of the verifier."""
    yield 64_000_000, 1_000_000_000
    yield 1_000_000_000, 5_000_000_000
    start = 5_000_000_000
    while start < min(end, 10**12):
        stop = min(start + 10**10, 10**12, end)
        yield start, stop
        start = stop
    while start < end:
        stop = min(start + 10**11, end)
        yield start, stop
        start = stop


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path, help='four columns: near far nodes leaves')
    p.add_argument('--checker', type=Path, default=HERE/'gateway_758')
    p.add_argument('--jobs', type=int, default=1)
    p.add_argument('--row', type=int, help='replay only this one-based band number')
    args = p.parse_args()
    rows = [tuple(map(int, line.split())) for line in args.manifest.read_text().splitlines()]
    if not rows or any(len(row) != 4 for row in rows) or args.jobs < 1:
        p.error('expected four columns per row and a positive worker count')
    end = rows[-1][1]
    if [r[:2] for r in rows] != list(bands(end)):
        p.error('manifest must exactly cover the prescribed partition from 64 million')
    if any(nodes != 2*leaves-1 or leaves < 1 for lo,hi,nodes,leaves in rows):
        p.error('invalid bisection counts')
    if args.row is not None:
        if not 1 <= args.row <= len(rows):
            p.error('row is outside the manifest')
        chosen = rows[args.row-1:args.row]
    else:
        chosen = rows
    def replay(row):
        lo, hi, _, _ = row
        proc = subprocess.run([str(args.checker.resolve()), '--universal', str(hi), str(lo)],
                              check=True, text=True, capture_output=True)
        result = tuple(map(int, proc.stdout.split()))
        if result != row:
            raise ValueError(f'Expected {row}, got {result}')
        return lo, hi
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for lo, hi in pool.map(replay, chosen):
            print(f'Checked offsets {lo} through {hi}', flush=True)
    if args.row is None:
        print(f'Checked all {len(rows)} bands from offset 64,000,000 through {end:,}.')


if __name__ == '__main__':
    main()
