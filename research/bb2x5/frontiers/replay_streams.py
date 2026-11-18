#!/usr/bin/env python3
"""Recreate a checked-in boundary-stream checkpoint from the blank tape."""
import argparse
import json
from pathlib import Path

from longitudinal import DRIVERS, Driver, ROOT
from checkpoints import checksum


def join_prefixes(words, batch, limit):
    words.extend('' for _ in range(len(batch)-len(words)))
    for i,word in enumerate(batch):
        words[i] += word[:limit-len(words[i])]


def trace_record(state,limit,words):
    payload = {'format':'bb2x5-entry-prefixes-v1','line':state['line'],'machine':state['machine'],
               'groups':state['groups'],'steps':state['steps'],'checkpoint_sha256':checksum(state),
               'prefix_length':limit,'entry_prefixes':words}
    return {'payload':payload,'sha256':checksum(payload)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--line', type=int, choices=DRIVERS, required=True)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--max-bits', type=int, default=1 << 30)
    parser.add_argument('--until-groups',type=int,help='stop at this absolute group count within the saved recipe')
    parser.add_argument('--trace-prefix',type=int,default=0,help='output the first K lifetime entries per cell as JSON')
    args = parser.parse_args()
    driver = Driver(args.line)
    state = driver.blank()
    expected = driver.load(ROOT/'frontiers/runs'/f'stream-{args.line:02}.json')
    target = expected['groups'] if args.until_groups is None else args.until_groups
    if not 0 <= target <= expected['groups'] or not 0 <= args.trace_prefix <= 65536:
        parser.error('group target outside the saved run or invalid prefix length')
    recipes = json.loads((ROOT/'frontiers/stream-recipes.json').read_text())
    words = []
    for row in recipes[str(args.line)]:
        repetitions, groups, finite_slots = row if len(row)==3 else (*row,0)
        for _ in range(repetitions):
            remaining = target-state['groups']
            if not remaining: break
            state,part = driver.run_batch(args.engine,state,min(groups,remaining),args.max_bits,args.trace_prefix,finite_slots)
            if args.trace_prefix:
                join_prefixes(words,part,args.trace_prefix)
    if state['groups'] != target or (target==expected['groups'] and state!=expected):
        parser.exit(1, 'Replay differs from saved checkpoint.\n')
    if args.trace_prefix:
        print(json.dumps(trace_record(state,args.trace_prefix,words),indent=2))
    elif target==expected['groups']:
        print(f"Line {args.line} agrees from blank at exactly {state['steps']} raw steps.")
    else:
        print(f"Line {args.line} reached {target} groups at exactly {state['steps']} raw steps.")


if __name__ == '__main__':
    main()
