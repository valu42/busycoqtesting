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
EXTRA_PREFIX = "PJPJ"
PREVIOUS = GATES_NEW[20][1]
# Historical cutoff used by the ordinary-header and clock certificates.
FAR = 61_410_570_681_246_030_619
EXTENDED_FAR = 64_916_341_784_245_418_891


def first_unchecked(covered):
    """The leftmost untested cylinder meeting depth 63 with 29 or 30 pairs."""

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


def check_rows(prefix, filename, worker):
    receipt = (HERE/filename).read_text()
    if worker:
        actual = subprocess.check_output([str(worker.resolve()), '63', '63', '29', '248', prefix], text=True)
        assert actual == receipt
    rows = [list(map(int, row.split())) for row in receipt.splitlines()[1:]]
    # The prefix is fixed. The remainder either ends at 63, or a final pair
    # follows a remainder ending at 62. Pascal's identity combines the counts.
    used_pairs = prefix.count('P')
    used = len(prefix) + used_pairs
    expected = {}
    for p in range(29,33):
        left = p-used_pairs
        n = 64-used-left
        if 0 <= left <= n:
            expected[p] = comb(n,left)
    assert len(rows) == len(expected) and {row[1] for row in rows} == set(expected)
    for r, p, guard, cells, probes, tests, exact, survivors in rows:
        assert (r, guard, survivors) == (63,248,0)
        assert cells == expected[p] and probes >= tests >= exact > 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--headers', type=Path, help='replay the restricted high-pair rows')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with integer assertions enabled')
    check_rows('PJJ', 'halting_collar_headers_758.tsv', args.headers)
    check_rows(EXTRA_PREFIX, 'halting_collar_extension_758.tsv', args.headers)
    absolute = (HERE/'high_pair_headers_758.tsv').read_text().splitlines()[1:]
    full = {row[1]:row for row in (list(map(int,r.split())) for r in absolute) if row[0]==63}
    assert all(full[p][2] == 248 and full[p][3] == comb(63-p, p-1) and full[p][-1] == 0 for p in (31,32))

    # The pre-alignment h0 increases weakly with even distance, and the
    # maximal jump count decreases weakly. Equal endpoint counts fix it.
    for distance in (PREVIOUS, EXTENDED_FAR-1):
        check_word(H-distance, PREFIX)
        assert aligned(distance)[2] == 244
    for distance in (PREVIOUS+1, EXTENDED_FAR):
        assert 0 < check_word(H-distance, EVEN_WORD) <= 615
    cutoff, word = first_unchecked(('PJJ', EXTRA_PREFIX))
    assert D*aligned(EXTENDED_FAR-1)[0] < POWER*cutoff <= D*aligned(EXTENDED_FAR+1)[0]
    assert horizon(EXTENDED_FAR) >= 248
    assert all(ancestry == 0 for _, _, ancestry in guard_counts(63,EXTENDED_FAR,252))
    tails = read_tails(28)
    assert sum(map(len,tails.values())) == 972
    margin = least_tail_margin(tails)
    assert POWER*margin > D*3**64*(EXTENDED_FAR+2000)
    # Low-count ordinary exits occur by 64+188, or are one of the 972
    # individually shadowed tails. Every positive return shortens countdown.
    assert 9*(len(PREFIX)+244+64+243+2) < 2*4000 < 2*(PREVIOUS-NEAR)
    print(f'All {EXTENDED_FAR-NEAR+1:,} reset seeds at distances {NEAR:,} through {EXTENDED_FAR:,} halt.')
    print(f'{EXTENDED_FAR-FAR:,} additional consecutive seeds beyond the previous collar. First unchecked cylinder starts with {word}.')


if __name__ == '__main__':
    main()
