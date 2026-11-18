#!/usr/bin/env python3
"""Enumerate actual finite mark prefixes compatible with full register tallies."""
import argparse
from itertools import combinations
from pathlib import Path


def transfer(marks, length):
    """One clear-start homogeneous digit, including a cut inside a burst."""
    v, pending = 1, False
    count = calls = interior = 0
    output = []
    for t in range(1, length + 1):
        marked = t in marks
        if marked and pending:
            raise ValueError('overlapping marked bursts')
        compound = marked or pending
        if compound and v == 1:
            output.append(count + 2)
        count += ((0, 0, 1), (1, 2, 2))[compound][v]
        calls += (4, 3, 3)[v] if compound else 1
        interior += ((0, 0, 2), (2, 6, 4))[compound][v]
        pending = compound and v != 0
        v = (v + 1 + compound) % 3
    return (v, int(pending), count, calls, interior), tuple(output)


def project(rows, start, last, locked):
    if not 53 <= start <= last < 403:
        raise ValueError('expected cuts in the homogeneous band')
    n, interior = rows[start - 1][2], rows[start - 1][4]
    total = interior // 2 - n
    if n < locked[-1] or total < len(locked):
        raise ValueError('probe beyond observed prefix')
    count = total - len(locked)
    results = {i: set() for i in range(start, last + 1)}
    # Remove mandatory three unmarked slots between neighboring candidates
    # before generating combinations, then reinsert them at their original offsets.
    end = n - 3 * max(0, count - 1)
    for values in combinations(range(locked[-1] + 4, end + 1), count):
        word = locked + tuple(v + 3 * i for i, v in enumerate(values))
        length = n
        observations = []
        for i in range(start, last + 1):
            observations.append(word)
            row, word = transfer(word, length)
            if row != rows[i]:
                break
            length = row[2]
        else:
            for i, candidate in enumerate(observations, start):
                results[i].add(candidate)
    if not results[start]:
        raise ValueError('no physical prefix satisfies the tallies')
    return results


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rows', type=Path)
    p.add_argument('--start', type=int, default=162)
    p.add_argument('--through', type=int, default=168)
    p.add_argument('--known-marks', nargs='+', type=int, default=[5, 11, 17, 23])
    args = p.parse_args()
    rows = [tuple(map(int, line.split())) for line in args.rows.read_text().splitlines()
            if not line.startswith('epochs ')]
    results = project(rows, args.start, args.through, tuple(args.known_marks))
    for cut, candidates in results.items():
        print('cut', cut, 'compatible prefixes', len(candidates), *sorted(candidates)[:4])
