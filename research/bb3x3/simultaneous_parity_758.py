"""Construct intervals of long ordinary prefixes for both launch parities of #758."""
import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import ceil, floor
from pathlib import Path
import subprocess

from annular_skip_758 import openings
from check_bb33 import HALTING_TARGET, first_return
from check_power_crossings_758 import read_report
from double35_frontier_758 import CUTS, TABLE, read_table
from scale_clauses_758 import check_word


@dataclass(frozen=True)
class Cylinder:
    left: Fraction
    right: Fraction
    word: str = ''
    depth: int = 0

    @property
    def width(self):
        return self.right - self.left

    def child(self, op):
        if op == 'J':
            return Cylinder(self.left, self.left + self.width/3, self.word + op, self.depth+1)
        assert op == 'P'
        return Cylinder(self.left + 5*self.width/9, self.right, self.word + op, self.depth+2)

    def overlap(self, other):
        return min(self.right, other.right) - max(self.left, other.left)


def cylinder(word, scale, depth=None):
    cell = Cylinder(Fraction(0), Fraction(scale))
    for op in word:
        if depth is not None and cell.depth >= depth:
            break
        cell = cell.child(op)
    return cell


def check_periodic_points():
    for size in range(1, 11):
        for word in product('JP', repeat=size):
            cell = cylinder(word, 1)
            fixed = cell.left / (1 - cell.width)
            if 'P' in word:
                assert fixed.numerator % 2 and fixed.denominator % 2
                assert (Fraction(3,2)*fixed).denominator % 2 == 0
            else:
                assert fixed == 0


def bands(n):
    assert n >= 10
    scale = Fraction(3, 2)
    odd, even = cylinder('PPPPP', 1), cylinder('PJPJ', scale)
    while min(odd.depth, even.depth) < n:
        assert odd.overlap(even) > 0 and Fraction(1,3) <= odd.width/even.width <= 3
        split_odd = odd.width > even.width
        cell, other = (odd, even) if split_odd else (even, odd)
        best = max((cell.child(op) for op in 'JP'), key=other.overlap)
        assert best.overlap(other) > 0
        if split_odd:
            odd = best
        else:
            even = best
    odd, even = cylinder(odd.word, 1, n), cylinder(even.word, scale, n)
    assert all(n <= w.depth <= n+1 for w in (odd, even))
    assert odd.overlap(even) >= Fraction(1, 2*3**(n+1))
    return odd, even


def window(m, n):
    odd, even = bands(n)
    p = 3**m
    pad = Fraction(32, p)
    a = max(odd.left, even.left) + pad
    b = min(odd.right, even.right) - pad
    assert 0 < a < b < 1
    low, high = ceil(p/b)-2*m, floor(p/a)-2*m
    assert low <= high
    for parity, cell in ((1, odd), (0, even)):
        for seed in (low+(parity-low)%2, high-(high-parity)%2):
            launch = openings(seed)
            assert launch.k == m-(1-parity)
            t = seed+4*(1-parity)+2*launch.k
            x = Fraction(launch.h, t) * (1 if parity else Fraction(3,2))
            margin = min(x-cell.left, cell.right-x)
            physical_margin = t * margin * (1 if parity else Fraction(2,3))
            assert physical_margin >= 20
            check_word(seed, ('I' if not parity else '') + 'J'*launch.k + cell.word.replace('P','LL'))
    return low, high, odd, even


# A shortened cut inside an existing, blank-reachable certificate row.
# Exponent: elementary suffix depth, previous row, cut receipt, two parity counts, first exit.
CASES = {
    34: (44, 135,
         (16949181699675672,16949613841245601,16949613841245761,16949613841245761,7594,18406594),
         (277,338),16949613841383425),
    35: (45, 162,
         (50846545099034461,50848841523849635,50848841523849749,50848841523849749,88866,168007533),
         (829,479),50848841524150265),
}


def verify_blank(m, worker):
    n, index, receipt, expected, exit_seed = CASES[m]
    low, high, odd, even = window(m, n)
    start, cut, seed, last, _, _ = receipt
    if m == 34:
        prior = read_report()['fourth'][index]
    else:
        rows = read_table(TABLE)
        assert all(i in rows for i in range(index+1)) and CUTS[index+1] == start
        prior = rows[index]
    assert prior[1] == start <= prior[2] <= prior[3] <= start+5000
    assert cut == low <= seed == last <= high
    if worker:
        out = subprocess.check_output([str(worker.resolve()),str(start),str(cut)],text=True)
        assert tuple(map(int,out.split())) == receipt
    counts = [0,0]
    while seed <= high:
        parity = seed%2
        suffix = (odd if parity else even).word.replace('P','LL')
        check_word(seed, ('I' if not parity else '')+'J'*(m-(1-parity))+suffix)
        counts[parity] += 1
        following = first_return(seed, batch=False)
        assert following is not None and following > seed
        seed = following
    assert tuple(counts) == expected and seed == exit_seed
    print(f'm={m}: [{low},{high}], {sum(counts)} consecutive blank origins, '
          f'{counts[0]} even and {counts[1]} odd, depth >= {n}.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker34',type=Path,help='replay the supplemental cut with cross_758_fast')
    parser.add_argument('--worker35',type=Path,help='replay the supplemental cut with the power-35 worker')
    args = parser.parse_args()
    if not __debug__:
        parser.error('assertions must be enabled')
    check_periodic_points()
    for m in (20, 21, 22, 23, 34, 35, 100, 292):
        low, high, _, _ = window(m, m-6)
        assert high-low >= 56
    for m in (34,35):
        verify_blank(m, getattr(args, f'worker{m}'))
    low, high, _, _ = window(292,492)
    assert high-low+1 == 204076 and high < HALTING_TARGET
    print(f'm=292: {high-low+1} origins below H, depth >= 492, blank entry unproved.')


if __name__ == '__main__':
    main()
