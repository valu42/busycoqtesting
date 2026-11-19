"""Match two-sided integer histories at any cut mass near the halting reset."""
from fractions import Fraction as F
from math import comb
from random import Random

from check_bb33 import HALTING_TARGET as H, champion_step

PAIR = ((5,20),(9,35),(7,26),(7,29))
LOW, HIGH = H-10**100, H+10**100


def future_interval(u, word, central=False):
    """Pull back the terminal midpoint and leave room for all rounding errors."""
    x, growth = F(1,4), F(1)
    for op in reversed(word):
        if op == 'J':
            x = (x+1)/3
            growth *= 3
        else:
            assert op == 'P'
            x *= F(4,9)
            growth *= F(9,4)
    radius = u/((8 if central else 4)*growth)-9
    assert radius > 0
    return u*x-radius, u*x+radius


def bulk(x, pairs):
    gain = 0
    for _ in range(pairs):
        v,b = PAIR[x%4]
        x = (9*x+b)//4
        gain += v
    return x,gain


def integer_ceil(x):
    return -(-x.numerator//x.denominator)


def bulk_witness(u, pairs, word):
    left,right = future_interval(u,word)
    l,h = 0,integer_ceil(left)
    while l<h:
        m = (l+h)//2
        if bulk(m,pairs)[0] < left:
            l = m+1
        else:
            h = m
    d,gain = bulk(l,pairs)
    assert left <= d <= right
    return u-gain,l,d


def prescribed_witness(u,past,word):
    """Find the first matching d for an exact fine past at the specified u."""
    l,h = future_interval(u,word,True)
    charges = [2 if op == 'J' else PAIR[int(op)][0] for op in past]
    x = u-sum(charges)
    z,m = 0,1
    for op,v in zip(past,charges):
        if op == 'J':
            m *= 3
            z = (3*z-x+1)%m
        else:
            m *= 9
            z = ((9*z+PAIR[int(op)][1])*pow(4,-1,m))%m
        x += v
    d = integer_ceil(l)+(z-integer_ceil(l))%m
    assert x == u and l <= d <= h
    initial = d
    for op,v in reversed(list(zip(past,charges))):
        x -= v
        if op == 'J':
            initial,r = divmod(initial+x-1,3)
        else:
            initial,r = divmod(4*initial-PAIR[int(op)][1],9)
            assert initial%4 == int(op)
        assert r == 0
    return x,initial,d


def replay(state,sequence):
    a,c = state
    for op in sequence:
        assert a > 1 and a%2 and c%2
        if op == 'J':
            assert a <= c
            a,c = champion_step(a,c)
        else:
            if op != 'P':
                assert (c-1)//2%4 == int(op)
            for _ in range(2):
                assert a >= 4*((c+1)//4)+3
                a,c = champion_step(a,c)
                assert a > 1
    return a,c


def audit():
    cases = ((150,100,100,234), (180,36,162,3))
    for a,j,p,quantity in cases:
        expansion = 3**j*F(9,4)**p
        mesh = F(9,4)**a
        assert (LOW/(2*expansion)-18)//(8*mesh) == quantity
        assert 9*a+10 < LOW
        print(2*a,'bulk calls before and',j+2*p,'calls after,',
              comb(j+p,j),'future words,',quantity,'states per word')
    for e,j,p,quantity in ((200,10,95,119_261),(110,100,100,2068)):
        expansion = 3**j*F(9,4)**p
        assert LOW/(8*expansion) > 100*3**e
        assert (LOW/(4*expansion)-18)//3**e == quantity
        print(e,'fine calls before and',j+2*p,'calls after,',
              comb(j+p,j),'future words,',quantity,'states per word')
    rng = Random(758)
    for u in (LOW,H,HIGH):
        for a,j,p,_ in cases:
            base = list('J'*j+'P'*p)
            for n in range(4):
                if n==1: base.reverse()
                if n>=2: rng.shuffle(base)
                s,d,expected = bulk_witness(u,a,base)
                mid = replay((2*s-4*d-1,2*d+1),'P'*a)
                assert mid == (2*u-4*expected-1,2*expected+1)
                replay(mid,base)
        for e,j,p in ((200,10,95),(110,100,100)):
            future = list('P'*p+'J'*j)
            for pair_count in (0,e//6,e//2):
                past = ['J']*(e-2*pair_count)+[str(rng.randrange(4)) for _ in range(pair_count)]
                rng.shuffle(past)
                rng.shuffle(future)
                s,d,expected = prescribed_witness(u,past,future)
                mid = replay((2*s-4*d-1,2*d+1),past)
                assert mid == (2*u-4*expected-1,2*expected+1)
                replay(mid,future)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions')
    audit()
