"""Certify an absolute extension of the scale-20 contiguous halting basin."""
import argparse
from fractions import Fraction
from math import comb
from pathlib import Path
import subprocess

from dyadic_guard_shadow_758 import guard_counts
from scale_clauses_758 import EVEN_WORD, H, PREFIX, check_word
from target_basin_758 import GATES_NEW, NEAR, least_tail_margin, read_tails
from target_shadow_758 import D, POWER, aligned, horizon

HERE = Path(__file__).resolve().parent
JUMPS = 2
PREVIOUS = GATES_NEW[20][1]
FAR = 61_410_570_681_246_030_619


def first_unchecked(jumps):
    """The leftmost untested cylinder meeting depth 63 with 29 or 30 pairs."""
    covered = 'P' + 'J'*jumps

    def visit(word, calls, pairs, a, four):
        if word.startswith(covered) or pairs > 30 or pairs + (64-calls)//2 < 29:
            return None
        if calls >= 63:
            if 29 <= pairs <= 30:
                return Fraction(a, 3**calls), word
            return None
        # J lies wholly to the left of P, even after any common prefix.
        return (visit(word+'J', calls+1, pairs, 3*a, four) or
                visit(word+'P', calls+2, pairs+1, 9*a+5*four, 4*four))

    return visit('P',2,1,5,4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--headers', type=Path, help='replay the restricted high-pair rows')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with integer assertions enabled')
    receipt = (HERE/'halting_collar_headers_758.tsv').read_text()
    if args.headers:
        actual = subprocess.check_output([str(args.headers.resolve()), '63', '63', '29', '248', str(JUMPS)], text=True)
        assert actual == receipt
    rows = [list(map(int, row.split())) for row in receipt.splitlines()[1:]]
    expected_pairs = {p for p in range(29,33) if 63-p-JUMPS >= p-1}
    assert {row[1] for row in rows} == expected_pairs and len(rows) == len(expected_pairs)
    for p in expected_pairs:
        hits = [row for row in rows if row[1] == p]
        assert len(hits) == 1
        r, _, guard, cells, probes, tests, exact, survivors = hits[0]
        assert (r, guard, survivors) == (63, 248, 0)
        assert cells == comb(63-p-JUMPS, p-1) and probes >= tests >= exact > 0
    absolute = (HERE/'high_pair_headers_758.tsv').read_text().splitlines()[1:]
    full = {row[1]:row for row in (list(map(int,r.split())) for r in absolute) if row[0]==63}
    assert all(full[p][2] == 248 and full[p][3] == comb(63-p, p-1) and full[p][-1] == 0 for p in (31,32))

    # The pre-alignment h0 increases weakly with even distance, and the
    # maximal jump count decreases weakly. Equal endpoint counts fix it.
    for distance in (PREVIOUS, FAR-1):
        check_word(H-distance, PREFIX)
        assert aligned(distance)[2] == 244
    for distance in (PREVIOUS+1, FAR):
        assert 0 < check_word(H-distance, EVEN_WORD) <= 615
    cutoff, word = first_unchecked(JUMPS)
    assert D*aligned(FAR-1)[0] < POWER*cutoff <= D*aligned(FAR+1)[0]
    assert horizon(FAR) >= 248
    assert all(ancestry == 0 for _, _, ancestry in guard_counts(63,FAR,252))
    tails = read_tails(28)
    assert sum(map(len,tails.values())) == 972
    margin = least_tail_margin(tails)
    assert POWER*margin > D*3**64*(FAR+2000)
    # Low-count ordinary exits occur by 64+188, or are one of the 972
    # individually shadowed tails. Every positive return shortens countdown.
    assert 9*(len(PREFIX)+244+64+243+2) < 2*4000 < 2*(PREVIOUS-NEAR)
    print(f'All {FAR-NEAR+1:,} reset seeds at distances {NEAR:,} through {FAR:,} halt.')
    print(f'{FAR-PREVIOUS:,} additional consecutive seeds. First unchecked cylinder starts with {word}.')


if __name__ == '__main__':
    main()
