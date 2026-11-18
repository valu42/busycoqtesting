#!/usr/bin/env python3
"""Recreate a checked-in boundary-stream checkpoint from the blank tape."""
import argparse
import json
from pathlib import Path

from longitudinal import DRIVERS, Driver, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--line', type=int, choices=DRIVERS, required=True)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--max-bits', type=int, default=1 << 30)
    args = parser.parse_args()
    driver = Driver(args.line)
    state = driver.blank()
    recipes = json.loads((ROOT/'frontiers/stream-recipes.json').read_text())
    for repetitions, groups in recipes[str(args.line)]:
        for _ in range(repetitions):
            state = driver.advance(args.engine, state, groups, args.max_bits)
    expected = driver.load(ROOT/'frontiers/runs'/f'stream-{args.line:02}.json')
    if state != expected:
        parser.exit(1, 'Replay differs from saved checkpoint.\n')
    print(f"Line {args.line} agrees from blank at exactly {state['steps']} raw steps.")


if __name__ == '__main__':
    main()
