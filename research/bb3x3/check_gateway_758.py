#!/usr/bin/env python3
"""Replay a chain of #758 gateways below the known halting basin.

Compile gateway_758.cpp as in GATEWAYS_758.md. A supplied cache stores
successful segment receipts for that executable and allows an interrupted run
to resume. Omit --cache for a fresh verification. Python 3.10 or later.
"""
import argparse
import hashlib
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import NamedTemporaryFile

from check_bb33 import HALTING_TARGET as H
from check_corridor_residues_758 import EVEN, ODD_PREFIX, check_word


# Decimal scale, exact far/near distances of the simple odd-word corridor,
# the second jump count, and the established gateway below its near endpoint.
GATES = {
    10: (15_333_300_998, 9_199_980_604, 264, 64_000_000),
    11: (137_999_708_986, 82_799_825_392, 262, 80_000_000_000),
    12: (1_241_997_380_866, 745_198_428_520, 260, 740_000_000_000),
    13: (11_177_976_427_786, 6_706_785_856_672, 258, 6_700_000_000_000),
}


def verify_gate(scale):
    far, near, jumps, _ = GATES[scale]
    for p, word in ((0, EVEN), (1, ODD_PREFIX + 'J'*jumps + 'LR')):
        low, high = H-far, H-near
        check_word(low+(p-low)%2, word)
        check_word(high-(high-p)%2, word)
    # In the even word the mass gain is at most 2*615. The odd word has
    # 293+jumps jumps, fifteen bulk moves and one return.
    assert (4*(293+jumps) + 9*15 + 5)//2 <= 5000


def segments(scale):
    # The shared spine connects every decimal milestone to the 64-million wall.
    result = [(10**10, 64_000_000)]
    for power, step in ((11, 5*10**9), (12, 10**10), (13, 10**11)):
        if power<=scale:
            result.extend((far, far-step) for far in range(10**power, 10**(power-1), -step))
    # A short branch from the near end of each long slab joins that spine.
    result.extend((near, join) for p, (_, near, _, join) in GATES.items() if p<=scale)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale',type=int,choices=GATES,default=10)
    parser.add_argument('--worker',type=Path,default=Path('./gateway_758'))
    parser.add_argument('--jobs',type=int,default=1)
    parser.add_argument('--cache',type=Path)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('assertions must be enabled and --jobs must be positive')
    worker=args.worker.resolve(strict=True)
    cache=args.cache
    if cache is not None:
        cache=cache/hashlib.sha256(worker.read_bytes()).hexdigest()
        cache.mkdir(parents=True,exist_ok=True)
    line_format=re.compile(r'nodes (\d+) returns (\d+) halts (\d+) remaining (\d+) '
                           r'maxgain (\d+)(?: exits (\d+)\.\.(\d+))?')

    def check(segment):
        far, near=segment
        target=cache/f'{far}-{near}.txt' if cache else None
        cached=target is not None and target.is_file()
        if cached:
            line=target.read_text().strip()
        else:
            line=subprocess.check_output([worker,str(far),str(near)],text=True).strip()
        match=line_format.fullmatch(line)
        if match is None:
            raise ValueError(f'unrecognized receipt for {far} to {near}')
        nodes, _, _, remaining, _, low, high=match.groups()
        if int(nodes)<1 or (int(remaining)==0)!=(low is None):
            raise ValueError(f'inconsistent receipt for {far} to {near}')
        if low is not None and not near-5000<=int(low)<=int(high)<near:
            raise ValueError(f'exit outside next gateway for {far} to {near}')
        if target is not None and not cached:
            with NamedTemporaryFile(mode='w', dir=target.parent, delete=False) as temp:
                temp.write(line+'\n')
            Path(temp.name).replace(target)
        return far, near

    corridor_low=(998*H+999)//1000
    check_word(corridor_low+corridor_low%2, EVEN)
    check_word(H-H%2, EVEN)
    for scale in GATES:
        if scale<=args.scale:
            verify_gate(scale)
    entries=segments(args.scale)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for index, (far,near) in enumerate(pool.map(check,entries),1):
            print(f'{index}/{len(entries)} verified distances {far} through {near}',flush=True)
    for scale, (far, near, _, _) in GATES.items():
        if scale<=args.scale:
            width=far-near+1
            print(f'All {width:,} reset seeds in [H-{far:,}, H-{near:,}] halt. '
                  f'Sufficient recent-reset bound: {(2*width)//9:,} calls.')


if __name__=='__main__':
    main()
