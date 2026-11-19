"""Exact reset and raw-clock skips at every sufficiently large power of three."""
from fractions import Fraction as F
from math import comb

from check_bb33 import champion_step
from timing_758 import branch_cost


MIN_EXPONENT = 20
MARGIN = 1000
DENOM = 64
# The shifted seed z=s+2m is compared with these multiples of P=3**m.
BANDS = {1: (F(1458,1475), 1), 2: (F(9,5), 2)}


def corridor(m, multiple):
    if m < MIN_EXPONENT or multiple not in BANDS:
        raise ValueError('choose m >= 20 and multiple 1 or 2')
    p = 3**m
    alpha, beta = BANDS[multiple]
    first = (alpha.numerator*p + alpha.denominator-1)//alpha.denominator
    return first + MARGIN - 2*m, beta*p - MARGIN - 2*m


def word(multiple, even):
    return 'LLJLLLR' if multiple == 1 and even else 'LR'


def margins(p, z, multiple, even):
    """Lower margins on physical counters and branch guards; affine in (p,z)."""
    if even:
        a = F(4*p,3)
    elif multiple == 1:
        a = F(2*p,3)
    else:
        a = F(2*p)
    c = z-a/2
    error = 3
    out = []
    for letter in word(multiple, even):
        out.extend((a-error-1, c-error))
        if letter == 'L':
            out.append(a-c-2*error-4)
            a, c = a-c, 3*c/2
            error = 2*error+7
        else:
            out.append(c-a-2*error)
            if letter == 'J':
                a,c = 3*a,c-a
                error = 3*error+2
    return out


def certify_all_exponents():
    p = 3**MIN_EXPONENT
    for multiple,(alpha,beta) in BANDS.items():
        for slope,offset in ((alpha,MARGIN),(beta,-MARGIN)):
            for even in (False, True):
                left = margins(p, slope*p+offset, multiple, even)
                right = margins(p+1, slope*(p+1)+offset, multiple, even)
                assert all(x > 0 and y >= x for x,y in zip(left,right))


def timed_word(seed, m, p, multiple):
    """Exact gain and raw time to first reset inside the proven corridor."""
    even = seed % 2 == 0
    a, c, clock = 1, seed, 0
    if even:
        clock = branch_cost(a,c)
        a,c = champion_step(a,c)
    k = m-1 if even or multiple == 1 else m
    power = p//3 if k == m-1 else p
    u, mass = a+1, a+2*c
    twice_clock = (6*u**2*((power**2-1)//8) - 17*u*((power-1)//2)
                   + k*(23+5*mass) + 10*k*(k-1))
    assert twice_clock % 2 == 0
    clock += twice_clock//2
    a,c = power*u-1, c-u*((power-1)//2)+2*k
    assert c >= 1
    for op in word(multiple, even):
        assert a > 1 and c % 2
        if op == 'L':
            assert a >= 4*((c+1)//4)+3
        else:
            assert a <= c and (a%2 == 1) == (op == 'J')
        clock += branch_cost(a,c)
        a,c = champion_step(a,c)
    assert a == 1 and 0 < c-seed <= 2*m+29
    return c,clock


def skip(m, multiple, start=None):
    """Advance to the first reset above the upper endpoint, with its exact clock."""
    lo,hi = corridor(m,multiple)
    seed = lo if start is None else start
    if not lo <= seed <= hi:
        raise ValueError('start outside the proven corridor')
    p = 3**m
    evaluations = 0

    def advance(s):
        nonlocal evaluations
        evaluations += 1
        assert lo <= s <= hi
        return timed_word(s,m,p,multiple)

    count = clock = 0
    seen = {}
    while seed <= hi and seed%DENOM not in seen:
        seen[seed%DENOM] = seed,count
        seed,dt = advance(seed)
        count += 1
        clock += dt
    if seed <= hi:
        old,index = seen[seed%DENOM]
        stride,length = seed-old,count-index
        assert stride > 0 and stride % DENOM == 0
        copies = (hi-seed)//stride
        if copies >= 3:
            sample = []
            for j in range(3):
                s = seed+j*stride
                time = 0
                for _ in range(length):
                    s,dt = advance(s)
                    time += dt
                assert s == seed+(j+1)*stride
                sample.append(time)
            v0,v1,v2 = sample
            clock += copies*v0 + comb(copies,2)*(v1-v0) + comb(copies,3)*(v2-2*v1+v0)
            seed += copies*stride
            count += copies*length
        while seed <= hi:
            seed,dt = advance(seed)
            clock += dt
            count += 1
    assert evaluations <= 5*DENOM
    return seed,count,clock,evaluations


def audit():
    certify_all_exponents()
    for m in (20,34,292):
        for multiple in BANDS:
            lo,hi = corridor(m,multiple)
            for start in (lo, lo+1, hi-70_000, hi-70_001):
                end,clock = timed_word(start,m,3**m,multiple)
                a,c,raw = 1,start,0
                while True:
                    raw += branch_cost(a,c)
                    a,c = champion_step(a,c)
                    if a == 1:
                        break
                assert (end,clock) == (c,raw)
            # This starting point admits a literal multi-cycle timing comparison.
            start=hi-70_000
            end,count,clock,_ = skip(m,multiple,start)
            s,n,t=start,0,0
            while s <= hi:
                s,dt = timed_word(s,m,3**m,multiple)
                n += 1
                t += dt
            assert (end,count,clock) == (s,n,t)


if __name__ == '__main__':
    from decimal import Decimal

    if not __debug__:
        raise SystemExit('Enable assertions.')
    audit()
    for m in (20,34,292,1000):
        for multiple in BANDS:
            _,count,clock,calls = skip(m,multiple)
            print(f'm={m}, gate={multiple}: {Decimal(count):.9E} resets, '
                  f'{Decimal(clock):.9E} raw steps, {calls} timed-word evaluations')
