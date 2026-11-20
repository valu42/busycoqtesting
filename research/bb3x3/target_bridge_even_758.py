#!/usr/bin/env python3
"""Check the enlarged even-coordinate target criterion and its lattice receipt."""
import argparse
from pathlib import Path
import subprocess

from target_basin_758 import GATES_NEW, NEAR, least_tail_margin, read_tails
from target_shadow_758 import D, POWER
from scale_clauses_758 import H

HERE = Path(__file__).resolve().parent
FAR = GATES_NEW[20][1]
MAX_H = 2 * (3**57 // (2 * D))
LAST_GUARD = 248
MAX_CALLS = 553
UPPER_TRIM = 9 * MAX_CALLS // 2


def verify(worker=None):
    assert MAX_H == 112_473_097_570_044_405_002
    assert 3**250 * MAX_H <= H - FAR
    assert 2 * 3**293 > H - NEAR - UPPER_TRIM + 2*293
    # k >= 250; all inverse guards through depth 248 are separated by
    # at least 3^min(k,307-depth-2)/D from an even aligned coordinate.
    assert 3**(307-LAST_GUARD-2) > D*(FAR+2600)
    assert 58+188 <= LAST_GUARD
    margin = least_tail_margin(read_tails(28))
    clearance = POWER*margin/(D*3**58)
    assert clearance > FAR+2600
    assert 307+1+243+2 == MAX_CALLS
    assert UPPER_TRIM == 2488
    # The only first cut with 29 pairs at r<=57 is P^29 at depth 58.
    a = 3**58 - 4**29
    step = 6*D
    first = (-a) % step
    assert 0 < first < 4**29 and first % 10 == 5 and step % 10 == 0
    assert a % 5 == 0
    eligible = (4**29-1-first)//step + 1
    receipt = (HERE/'target_bridge_even_lattice_758.tsv').read_text()
    rows = receipt.splitlines()
    assert rows[0].split() == ['r','p','last_guard','cells','probes','angular_tests','exact_fallbacks','survivors']
    assert len(rows) == 2
    assert tuple(map(int,rows[1].split())) == (57,29,248,1,103848245,103822208,42425,0)
    if worker:
        actual = subprocess.check_output([str(worker.resolve()), '57', '57'],text=True)
        assert actual == receipt
    allowed_masses = ((H-NEAR-UPPER_TRIM)//2)-((H-FAR-1)//2)
    states = allowed_masses*(MAX_H//2)
    print(f'Every even h from 2 through {MAX_H:,} returns inside the scale-20 basin within {MAX_CALLS} calls.')
    print(f'The sole high-pair cylinder has {eligible:,} admissible lattice directions; all escape by aligned depth {LAST_GUARD}.')
    print(f'Listed lower-pair tails clear the physical guards by at least {int(clearance):,} aligned units.')
    print(f'The enlarged rectangle contains {states:,} ordinary states.')
    if not worker:
        print('Using the archived lattice receipt; supply --worker for its exhaustive replay.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path)
    args = parser.parse_args()
    verify(args.worker)
