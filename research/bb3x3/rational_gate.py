"""Check a rational, real-guarded counterexample to finite-prime relaxations."""
from fractions import Fraction as F
from math import gcd, isqrt

from check_bb33 import HALTING_TARGET as H
from scale_clauses_758 import BASE


N = 20
M = 4**N
Q = 3*9**N
DEN = Q-M
G = BASE*3**74
MID = H-5*G//4


def prime_certificate():
    # Lucas primality criterion; the order of 2 modulo DEN is exactly DEN-1.
    factors = (2,107,541193,314923802363)
    prod = 1
    for p in factors:
        assert all(p%div for div in range(2,isqrt(p)+1))
        prod *= p
    assert prod == DEN-1 and pow(2,DEN-1,DEN) == 1
    assert all(gcd(pow(2,(DEN-1)//p,DEN)-1,DEN) == 1 for p in factors)
    assert DEN > 2**64


def graph():
    # Accumulate (3*9^20*d+A*u+C)/4^20 through J and then 20 bb pairs.
    a,c,m,v = -1,1,1,2
    for _ in range(N):
        a,c,m,v = 9*a,9*c+20*m,4*m,v+5
    assert m == M and v == 102
    slope = F(-a,DEN)
    offset = (m*slope*v-c)/DEN
    assert slope == F(9**N,DEN) and offset.denominator == DEN**2
    return slope,offset


def mod4(r):
    assert gcd(r.denominator,4) == 1
    return r.numerator*pow(r.denominator,-1,4)%4


def audit():
    prime_certificate()
    slope,offset = graph()
    first = MID-102*((MID-(H-2*G))//102+1)
    assert first <= H-2*G < first+102
    u = first
    a,b = slope,offset
    assert (a*u+b).denominator == DEN**2
    # Test real guards for all u>=first by testing their margins and slopes.
    assert 3*a>1 and 2*a<1 and 3*(a*u+b)>=u-1 and 2*(a*u+b)<=u-1
    a,b,u = 3*a-1,3*b+1-2*(3*a-1),u+2
    for _ in range(N):
        assert a>0 and 9*a<2 and 9*(a*u+b)<=2*u-12 and a*u+b>0
        assert mod4(a)==mod4(b)==0
        a,b,u = 9*a/4,(9*b+20)/4-5*(9*a/4),u+5
    assert u==first+102 and (a,b)==(slope,offset)
    assert (MID-first)%102 == 0


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    audit()
    print("The rational J(bb)^20 path satisfies all tested real and congruence guards.")
