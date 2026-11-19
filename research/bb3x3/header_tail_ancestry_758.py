#!/usr/bin/env python3
"""Recover exact reset offsets for a specified exceptional dyadic direction."""
from collections import defaultdict
from functools import cache
import argparse
import csv
from pathlib import Path

from scale_transport_758 import H, PERIOD, prefix
from check_bb33 import champion_step

DIVISOR = 13_959_275
DEFAULT_TAILS = Path(__file__).with_name("dyadic_long_tails_758.tsv")


def long_tails(path):
    groups = defaultdict(list)
    with path.open() as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            assert int(row["length"]) >= 189
            groups[int(row["p"])].append(int(row["numerator"]))
    return groups


def literal_return(d):
    start = H-d
    a, c = 1, start
    for calls in range(1, 10_001):
        result = champion_step(a,c)
        if result is None:
            return calls, "halt"
        a,c = result
        if a == 1:
            return calls, c-start
    raise RuntimeError(f"literal return unresolved at offset {d}")


@cache
def header_residues():
    offsets = defaultdict(list)
    for offset in range(0, PERIOD, 2):
        h = prefix(offset)[0]//2
        offsets[h % (2*DIVISOR)].append((offset, h))
    return offsets


def half_words(blocks, first_pair=False, last_pair=False):
    """Group endpoint numerators A by the pair count for all indicated words."""
    by_count = defaultdict(list)

    def extend(a, used, pairs):
        if used == blocks:
            by_count[pairs].append(a)
            return
        forced = (first_pair and used == 0) or (last_pair and used == blocks-1)
        if not forced:
            extend(3*a, used+1, pairs)
        extend(9*a + 5*4**pairs, used+1, pairs+1)

    extend(0, 0, 0)
    return by_count


def compatible_offsets(r, pairs, numerators):
    """All actual header offsets at this r realizing N/4^pairs at the cut."""
    answer = {n: set() for n in numerators}
    for m, scale in ((r, 1), (r+1, 3)):
        if m < 2*pairs:
            continue
        blocks = m-pairs
        left_blocks = blocks//2
        right_blocks = blocks-left_blocks
        if left_blocks == 0:
            raise ValueError("need at least two blocks at the cut")
        left_words = half_words(left_blocks, first_pair=True)
        right_words = half_words(right_blocks, last_pair=(m != r))
        modulus = 2*scale*DIVISOR
        for left_pairs, left_constants in left_words.items():
            right_pairs = pairs-left_pairs
            if right_pairs not in right_words:
                continue
            cut_multiplier = 3**(right_blocks+right_pairs)
            by_residue = defaultdict(list)
            for a in left_constants:
                term = a*cut_multiplier
                by_residue[term % modulus].append(term)
            for a in right_words[right_pairs]:
                term = 4**left_pairs*a
                for n in numerators:
                    for left in by_residue.get((-term-n) % modulus, ()):
                        h = (left+term+n)//(scale*DIVISOR)
                        for offset, base_h in header_residues().get(h % (2*DIVISOR), ()):
                            answer[n].add(offset + PERIOD*((h-base_h)//(2*DIVISOR)))
    return answer


def verify():
    # Positive tests include both possible alignment depths.
    for r, d, n, p, depth in (
        (44, 54_516_211_208, 15_527_857_315, 17, 45),
        (53, 1_607_924_367_951_120, 572_363_396_515, 20, 54),
        (60, 3_560_530_549_613_693_714, 157_763_151_949_265, 25, 60),
    ):
        a, b = DIVISOR*(prefix(d)[0]//2), 3**r
        elapsed = pairs = 0
        while elapsed < r:
            if 3*a < b:
                a *= 3
                elapsed += 1
            else:
                assert 9*a > 5*b
                a, b = 9*a-5*b, 4*b
                elapsed += 2
                pairs += 1
        assert elapsed == depth and pairs == p and a*4**p == b*n
        assert d in compatible_offsets(r,p,(n,))[n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("r", type=int, nargs="?")
    parser.add_argument("p", type=int, nargs="?")
    parser.add_argument("numerators", type=int, nargs="*")
    parser.add_argument("--tails", type=Path, default=DEFAULT_TAILS)
    args = parser.parse_args()
    if args.r is not None:
        if args.p is None or not args.numerators:
            parser.error("specify r, p and one or more numerators")
        print(compatible_offsets(args.r,args.p,args.numerators))
    else:
        verify()
        print("r\tp\tnumerator\toffset\tcalls\treset_gain")
        for p, numerators in long_tails(args.tails).items():
            for r in range(2*p-1, 61):
                found = compatible_offsets(r,p,numerators)
                for n in numerators:
                    for d in sorted(found[n]):
                        calls, gain = literal_return(d)
                        print(r,p,n,d,calls,gain,sep="\t")
