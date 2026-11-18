#!/usr/bin/env python3
"""Meet a saved line 15 boundary one full driver period later using window.cpp."""
import argparse
import base64
from itertools import zip_longest
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryFile
import zlib

from line15 import Left, MACHINE, advance, load


def physical(driver, groups, positive):
    """Build both physical tape halves without expanding the raw clock."""
    _, pieces = driver.left(driver.excursions(groups))
    negative = bytearray()
    for copies, blocks in pieces:
        word = bytes(d for block in blocks for d in reversed(block))
        negative.extend(word * copies)
    left = -len(negative)
    negative.reverse()
    return left, negative + positive


def rows(left, tape):
    for match in re.finditer(rb'([\x01-\x04])\1*', tape):
        yield f'{left + match.start()} {match.end() - match.start()} {tape[match.start()]}\n'


def check(path, engine, window, budget):
    driver = Left()
    seed = load(path)
    groups = seed['groups']
    old = zlib.decompress(base64.b64decode(seed['positive_zlib_base64']))
    new, cost = advance(driver, engine, groups, groups+1, old, 10**7, seed['positive_steps'])
    end = driver.left(driver.excursions(groups+1))[0] + seed['positive_steps'] + cost
    left, first = physical(driver, groups, old)
    next_left, final = physical(driver, groups+1, new)

    # Stream the native run format. Deep records can have millions of runs.
    with TemporaryFile(mode='w+') as source:
        source.write(f"{MACHINE}\n{seed['steps']} 0 {'AB'.index(seed['state'])}\n")
        source.writelines(rows(left, first))
        source.seek(0)
        with subprocess.Popen([str(window.resolve()), '8', str(end), str(budget)], stdin=source,
                              stdout=subprocess.PIPE, text=True) as worker:
            out = worker.stdout
            status = out.readline().split()
            if len(status) != 2 or status[0] != 'unknown' or out.readline().strip() != MACHINE:
                raise ValueError('invalid window result')
            if out.readline().split() != [str(end), '0', str('AB'.index(driver.period[-1]))]:
                raise ValueError('window did not reach the next period in the expected state')
            if any(got != want for got, want in zip_longest(out, rows(next_left, final))):
                raise ValueError('physical tapes differ at the next period')
            if worker.wait():
                raise RuntimeError('native window replay failed')
    print(f"Matched both tape halves, head and state from group {groups} to {groups+1}, "
          f"{end-seed['steps']:,} raw steps ending at {end:,}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    parser.add_argument('--engine', type=Path, required=True, help='compiled line15_stream.cpp')
    parser.add_argument('--window', type=Path, required=True, help='compiled window.cpp')
    parser.add_argument('--work', type=int, default=400_000_000)
    args = parser.parse_args()
    check(args.checkpoint, args.engine, args.window, args.work)
