"""Certify a joint-cover exponent for bounded pair-count differences of machine 758."""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
import subprocess


@cache
def cells(depth):
    """Ordinary cylinders of this symbolic depth on the common grid 9**depth."""
    layer = [(0, 9**depth)]
    for _ in range(depth):
        children = []
        for a,b in layer:
            width = b-a
            assert width % 9 == 0
            children.extend(((a,a+width//3),(a+5*(width//9),b)))
        layer = children
    return layer


def merge(intervals):
    result = []
    for a,b in intervals:
        if not result or a > result[-1][1]:
            result.append((a,b))
        elif b > result[-1][1]:
            result[-1] = (result[-1][0],b)
    return result


DEN = 10**6
SIGMA = Fraction(13,20)
J_WEIGHT, P_WEIGHT = 489634,590312
PADDING = 10**9
MAX_DEPTH = 12
SLOPE_LIMIT = 400


def slopes(limit):
    for balance in range(-limit,limit+1):
        ratio = Fraction(3,2)*Fraction(4)**balance
        while ratio > 5:
            ratio /= 3
        while ratio <= Fraction(5,3):
            ratio *= 3
        yield balance, ratio


def unresolved(depth, ratio, previous):
    """Translations still exceeding unit total child weight at every tried depth."""
    scale = 9**depth
    # Translation units are 1/(ratio.denominator*PADDING*9**depth).
    p, q = ratio.numerator*PADDING, ratio.denominator*PADDING
    padding = scale*ratio.denominator
    source = cells(depth)
    even_lo = [a*p for a,b in source]
    even_hi = [b*p for a,b in source]
    weights = [J_WEIGHT**(depth-j)*P_WEIGHT**j for j in range(depth+1)]
    ceiling = DEN**depth
    remaining = []
    for old_lo,old_hi in previous:
        tlo,thi = 9*old_lo,9*old_hi
        events = []
        for i,(a,b) in enumerate(source):
            lo,hi = a*q-padding,b*q+padding
            first = bisect_left(even_hi,lo-thi)
            stop = bisect_right(even_lo,hi-tlo)
            # Reverse order makes the translation intervals increasing.
            hits = ((max(tlo,lo-even_hi[j]),min(thi,hi-even_lo[j])) for j in range(stop-1,first-1,-1))
            weight = weights[i.bit_count()]
            for left,right in merge(hits):
                events.extend(((left,0,weight),(right,1,-weight)))
        # Closed intervals require arrivals at an endpoint before departures.
        events.sort()
        mass, start, last = 0,None,None
        for position, _, change in events:
            if position != last and start is not None and mass <= ceiling:
                remaining.append((start,last))
                start = None
            mass += change
            if start is None and mass > ceiling:
                start = position
            last = position
        if start is not None:
            remaining.append((start,last))
        assert mass == 0
    return merge(remaining)


def certify(ratio):
    pad = ratio.denominator
    bins = [(-ratio.numerator*PADDING-pad,ratio.denominator*PADDING+pad)]
    for depth in range(1,MAX_DEPTH+1):
        bins = unresolved(depth,ratio,bins)
        if not bins:
            return depth
    raise AssertionError(f'no uniform certificate for slope {ratio}')


def single_count(m):
    @cache
    def count(depth,pairs):
        if 3**m * 4**pairs <= 3**depth:
            return 1
        return count(depth+1,pairs)+count(depth+2,pairs+1)
    return count(0,0)


ROWS = {
    # exponent: positive pairs, distinct odd, distinct even, total single-phase odd
    8: (81,74,70,949),
    12: (606,551,524,23058),
    16: (4652,4228,4041,560851),
    20: (35782,31745,31791,13643734),
    24: (277473,240672,251257,333841729),
    26: (770011,666149,699334,1665376507),
    30: (5927547,5173188,5341753,42467340908),
    34: (45686165,40585745,40479316,1096294154557),
    35: (76077049,67856170,67135504,2466287855329),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path,help='also regenerate all geometric-cover rows with the C++ worker')
    args = parser.parse_args()
    if not __debug__:
        parser.error('assertions must be enabled')
    a,b = SIGMA.numerator,SIGMA.denominator
    assert J_WEIGHT**b*3**a >= DEN**b and P_WEIGHT**b*9**a >= DEN**b*4**a
    assert 3*3**292*4**400 < 2*9**400  # even a 400-pair width is below the target unit
    depth_counts = Counter(certify(ratio) for _,ratio in slopes(SLOPE_LIMIT))
    print(f'sigma={SIGMA}, adversarial normalized padding +/-1/{PADDING}, depths {dict(sorted(depth_counts.items()))}')
    assert sum(depth_counts.values()) == 2*SLOPE_LIMIT+1 and max(depth_counts) <= MAX_DEPTH
    for m,(pairs,odd,even,total_odd) in ROWS.items():
        assert single_count(m) == total_odd
        if args.worker:
            output = subprocess.check_output([str(args.worker.resolve()),str(m)],text=True)
            assert tuple(map(int,output.split())) == (m,pairs,odd,even)
    print(f'At scale 3^-35, {ROWS[35][1]:,} of {ROWS[35][3]:,} odd cylinders contain a joint survivor.')


if __name__ == '__main__':
    main()
