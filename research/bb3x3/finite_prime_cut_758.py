"""Rational crossings realizing prescribed #758 instructions and prime tests."""
from fractions import Fraction as F
from math import gcd
from random import Random

from check_bb33 import HALTING_TARGET as H

PAIR = ((5,20),(9,35),(7,26),(7,29))


def period(tail,n):
    jumps = tail.count('J')
    pairs = len(tail)-jumps
    assert jumps+2*pairs <= 200 and n >= 3
    diff = 1+pairs-jumps
    repair = 'J'*max(diff,0)+'0'*max(-diff,0)
    return '0J'*n+tail+repair


def affine_graph(word):
    # d'=(K*d+A*u+C)/L and u'=u+V through the full word.
    K,A,C,L,V = 1,0,0,1,0
    for op in word:
        if op == 'J':
            K,A,C,V = 3*K,3*A-L,3*C+(1-V)*L,V+2
        else:
            v,b = PAIR[int(op)]
            K,A,C,L,V = 9*K,9*A,9*C+b*L,4*L,V+v
    q = K-L
    slope = F(-A,q)
    return q,V,slope,(L*V*slope-C)/q


def next_phase(op,slope,offset):
    if op == 'J':
        new = 3*slope-1
        return new,3*offset+1-2*new
    gain,b = PAIR[int(op)]
    new = 9*slope/4
    return new,(9*offset+b)/4-gain*new


def residue(x,m):
    return x.numerator*pow(x.denominator,-1,m)%m


def verify(tail,cut,n,excluded):
    word = period(tail,n)
    q,v,x,b = affine_graph(word)
    pairs = len(word)-word.count('J')
    assert word.count('J') == pairs+1 and q == 3*27**pairs-4**pairs
    assert gcd(6*excluded,q) == 1
    assert 0 < abs(x-F(4,23)) < F(4,27)**n/3
    assert x.denominator > v
    charges = [2 if op=='J' else PAIR[int(op)][0] for op in word]
    phase = 2*n+cut
    u = H-sum(charges[:phase])
    initial = x,b
    for i,op in enumerate(word):
        if i==phase:
            assert u == H
        assert q%x.denominator == 0 and q*q%b.denominator == 0
        assert -7 <= b <= 0 and (x*u+b).denominator > 1
        if not tail:
            assert F(4,27) <= x <= F(38,81)
            test_mass = 200
        else:
            assert min(x,F(1,2)-x) >= F(1,4*3**202)
            test_mass = 1000*3**202
        d = test_mass*x+b
        assert 2*d < test_mass-1 and d > 0
        if op == 'J':
            assert 3*x > 1 and 3*d >= test_mass-1
        else:
            r = int(op)
            assert 9*x < 2 and 9*d <= 2*test_mass-(12 if not tail else 18)
            assert residue(x,4) == 0 and residue(b,4) == r
        x,b = next_phase(op,x,b)
        u += charges[i]
    assert (x,b)==initial


def audit():
    for n,excluded in ((3,1),(4,5),(6,7),(22,23),(24,5*7*13),(40,5*11*41)):
        verify('',0,n,excluded)
    rng = Random(758)
    tails = ['J'*200,'3'*100,'1J3J'*30,'0J'*50+'J']
    mixed = list('J'*100+''.join(str(rng.randrange(4)) for _ in range(50)))
    rng.shuffle(mixed)
    tails.append(''.join(mixed))
    for tail in tails:
        short = period(tail,3)
        extra_pairs = len(short)-short.count('J')-3
        n = 24+(-extra_pairs)%12
        verify(tail,len(tail)//2,n,5*7)
    assert H-10**100 > 1000*3**202
    print('Six prime tests and five prescribed-word crossings passed.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions')
    audit()
