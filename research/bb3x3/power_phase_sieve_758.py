"""Exclude short terminal seam events over 10**100 exponents by counting phases."""
from fractions import Fraction as F
from functools import cache
from power_phase_law_758 import bulk_sequence, outcome

Q = 2**1024
LO, HI = 1500, 10**100
DEPTH = 8
TOL = Q//2**500


def ceildiv(a,b):
    return -(-a//b)


@cache
def series_log(x):
    """Integer enclosure of Q*ln(x) for rational x between 1 and 2."""
    assert 1 <= x <= 2
    y = (x-1)/(x+1)
    lo,hi = (y*Q).__floor__(), (y*Q).__ceil__()
    square_lo, square_hi = lo**2//Q, ceildiv(hi**2,Q)
    term_lo,term_hi = lo,hi
    sum_lo = sum_hi = 0
    for j in range(400):
        k = 2*j+1
        sum_lo += term_lo//k
        sum_hi += ceildiv(term_hi,k)
        term_lo = term_lo*square_lo//Q
        term_hi = ceildiv(term_hi*square_hi,Q)
    # 2*sum_{k>=801,odd} (1/3)^k/k < 3/3^801 < 1/Q.
    assert 3*Q < 3**801
    return 2*sum_lo,2*sum_hi+1


def log_bounds(x):
    x = F(x)
    e = 0
    while x<1:
        x *= 2
        e -= 1
    while x>=2:
        x /= 2
        e += 1
    l,h = series_log(x)
    a,b = series_log(F(2))
    return l+min(e*a,e*b),h+max(e*a,e*b)


def log_b_limits(x):
    l,h = log_bounds(x)
    a,b = log_bounds(F(3,2))
    assert a>0
    return min(Q*l//a,Q*l//b),max(ceildiv(Q*h,a),ceildiv(Q*h,b))


def floor_sum(n,m,a,b):
    """Sum floor((a*i+b)/m), i=0,...,n-1, by lattice transposition."""
    total = 0
    while True:
        aq,a = divmod(a,m)
        bq,b = divmod(b,m)
        total += aq*(n-1)*n//2 + bq*n
        height = a*n+b
        if height < m:
            return total
        n,b = divmod(height,m)
        a,m = m,a


def threshold_set(depth):
    level = {F(0),F(1,3),F(5,9),F(1)}
    result = set(level)
    for _ in range(depth):
        level = {y for x in level for y in (x/3,(4*x+5)/9)}
        result.update(level)
    return result


def run():
    for n in range(1,13):
        for m in range(1,9):
            for a in range(-5,8):
                for b in (-12,-1,0,13):
                    assert floor_sum(n,m,a,b)==sum((a*i+b)//m for i in range(n))
    # Compute rigorous bounds on the infinite-series constant from one integer.
    r=1
    j=2000
    for _ in range(j):
        r = 6*((r+1)//4)+5
    klo,khi = ((r+q)*F(2,3)**j for q in (7,13))
    aa,ab = log_b_limits(3)
    aa = (aa+ab)//2
    deltas = threshold_set(DEPTH)
    n = HI-LO+1
    for x in deltas:
        # The forbidden congruence is m*log_b3+log_b(2(3-x)/(3K)) = 0 (mod 1).
        bl = log_b_limits(2*(3-x)/(3*khi))[0]
        bh = log_b_limits(2*(3-x)/(3*klo))[1]
        b = (bl+bh)//2
        assert HI*(ab-aa+1)+max(b-bl,bh-b) < TOL//2
        tol = 2*TOL
        base = LO*aa+b+tol
        count = floor_sum(n,Q,aa,base)-floor_sum(n,Q,aa,base-2*tol-1)
        assert count==0,(x,count)
    right,debit = bulk_sequence(4*3**LO)
    for m in range(20,LO):
        result = outcome(m,right,debit,DEPTH)
        assert 'boundary' not in result and 'seam' not in result
    # Elementary numerical margins applied uniformly in the proof.
    assert 2**510 * 2000*(LO+1)*3**DEPTH < 3**LO
    print(f'{len(deltas)} phase thresholds avoided for {LO} <= m <= 10^100.')
    print(f'All 20 <= m < {LO} checked on the integer map.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    run()
