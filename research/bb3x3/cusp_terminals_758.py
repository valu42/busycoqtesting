"""Verify the exact fifteen-bulk terminal family in the reset-density cusp."""
from fractions import Fraction
from check_bb33 import champion_step, first_return

Q = 2**15
D = 3**16-2**16
BASE_I = 28_826
BASE_P = 75_627_293
PERIOD = 1200


def affine_tail(i):
    # The first left counter below suppresses its additive 2P term.
    a, c = -4*i-4, 6*i+5
    for _ in range(14):
        q = (c+1)//4
        a, c = a-4*q-3, 6*q+5
    return a, c


def candidate(m):
    p = 3**m
    assert m >= 597 and m % PERIOD == 597
    number, remainder = divmod(p-BASE_P, 2*D)
    assert remainder == 0
    i = BASE_I+Q*number
    return p-2*m+4*i-2


def verify():
    acceptable = {}
    for i in range(Q):
        a, c = affine_tail(i)
        high_a, high_c = affine_tail(i+Q)
        assert high_c % 4 == c % 4
        assert (high_c-high_a)-(c-a) == 4*D
        for gap in (1,3):
            if gap == 3 and c % 4 != 3:
                continue
            base = (c-a+gap)//2
            assert 2*base == c-a+gap
            acceptable.setdefault(base % (2*D), []).append((i,gap))
    seen = set()
    hits = []
    p = 1
    while p not in seen:
        m = len(seen)
        seen.add(p)
        for i, gap in acceptable.get(p, ()):
            hits.append((m,i,gap))
        p = 3*p % (2*D)
    assert p == 1 and len(seen) == PERIOD
    assert hits == [(597,BASE_I,1)]
    a,c = affine_tail(BASE_I)
    assert 2*BASE_P+a == c+1
    assert Fraction(1) < 1+Fraction(2*Q,D) < Fraction(251,250)
    ratio = Fraction(3,2)**15
    center = 1+Fraction(2*Q,D)
    slope = (3*ratio-2)/(2*center)
    assert Fraction(1,3) < slope*Fraction(54,100)/729
    assert slope*Fraction(58,100)*Fraction(101,100)/729 < Fraction(5,9)
    for m in (597,1797):
        s = candidate(m)
        assert first_return(s, batch=False) is None
        assert first_return(s+2, batch=False) is None
        p = 3**m
        for start in (s,s+2):
            a,c = 2*p-1,start-p+1+2*m
            for _ in range(15):
                assert a >= 4*((c+1)//4)+3
                a,c = champion_step(a,c)
                assert a>1
            assert a==c+1 and a%2==0
    for d in (23,25):
        m=1797
        assert first_return(candidate(m)-2*m-d, batch=False)==candidate(m)
    print('One exponent class modulo 1,200, with two odd direct halts at each scale.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
