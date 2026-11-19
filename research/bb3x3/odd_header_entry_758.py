"""Verify the odd primitive header test throughout the scale-20 wall."""
import argparse
import subprocess
from collections import defaultdict
from functools import cache
from pathlib import Path

from even_header_entry_758 import tail
from nonreset_entry_758 import FAR, MAX_CALLS, MAX_GAIN, MAX_MASS, MIN_MASS
from target_shadow_758 import D, POWER

MAX_R = 45
MAX_H = (3**MAX_R-1)//D


@cache
def words(length):
    """All (intercept, pair count, ends with a pair) of this elementary length."""
    if length < 0:
        return []
    if length == 0:
        return [(0,0,False)]
    return ([(3*a,p,False) for a,p,_ in words(length-1)] +
            [(9*a+5*4**p,p+1,True) for a,p,_ in words(length-2)])


def ties(r):
    """Join the two halves of every first inverse preimage of the 5/9 guard."""
    length = r-2
    split = (length-2)//2  # remove the initial P
    hits = []
    for first in (split,split+1):
        second = length-2-first
        if second < 0:
            continue
        lookup = defaultdict(list)
        for a,p,_ in words(second):
            endpoint = 9*a + 5*4**p
            lookup[endpoint%D].append(endpoint)
        for a,p,ends_in_pair in words(first):
            if first > split and not ends_in_pair:
                continue
            a,p = 5*3**first + 4*a,p+1  # prepend P
            base,scale = 9*3**second*a,4**p
            residue = -base*pow(scale,-1,D)%D
            for endpoint in lookup[residue]:
                h, remainder = divmod(base+scale*endpoint,D)
                assert remainder == 0 and h%2 and h%3
                assert 3**(r-1) < D*h < 3**r
                hits.append(h)
    assert len(set(hits)) == len(hits)
    return sorted(hits)


def read_table(name, header):
    with Path(__file__).with_name(name).open() as f:
        assert next(f).strip() == header
        return [tuple(map(int,line.split())) for line in f]


def verify(worker=None):
    # At launch k=307-r; even or odd h has sufficient nonzero guard clearance.
    assert 3**14 < D < 3**15 and 3**307 == POWER
    assert 3**min(307-MAX_R,307-(MAX_R+1+176)-2) > D*(FAR+2600)
    assert 307+1+176+2 == 486 <= MAX_CALLS
    assert 9*486//2 <= MAX_GAIN
    assert MIN_MASS <= MAX_MASS
    recorded = read_table('odd_header_ties_758.tsv','r h')
    expected = [(r,h) for r in range(15,MAX_R+1) for h in ties(r)]
    assert expected == recorded and len(recorded) == 264
    assert sorted(h for _,h in recorded)[:3] == [1,14_365_291,43_063_105]
    rows = read_table('odd_header_tails_758.tsv','denominator_bits witness max_calls')
    assert [b for b,_,_ in rows] == list(range(3,MAX_R+1))
    for b,n,depth in rows:
        assert n%10 == 5 and 0<n<2**b and tail(n,2**b)==depth<=176
    if worker:
        query = ''.join(f'0 0 {b} 5 10\n' for b,_,_ in rows)
        result = subprocess.check_output([worker,'--bit-progressions'],input=query,text=True)
        assert [tuple(map(int,l.split())) for l in result.splitlines()] == [
            (0,0,b,5,10,n,depth) for b,n,depth in rows]
    size = (MAX_H+5)//6+(MAX_H+1)//6
    return size,len(recorded)-1


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('run without -O for verification')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path,help='compiled dyadic_survival_758.cpp to repeat the exact searches')
    args = parser.parse_args()
    size,exceptions = verify(args.worker.resolve() if args.worker else None)
    print(f'Of {size:,} odd primitive h through {MAX_H:,}, {exceptions} possible exceptions remain.')
