"""Exact dyadic accounting for P gaps and for Q at aligned line-26 checkpoints."""
from fractions import Fraction
from itertools import product

from column_tick import column, raw_tick
from prior_frontier import LIST, M26


def reserve(word):
    value = Fraction(0)
    for d in word:
        u,e = divmod(d,2)
        value = (value+1-u)/(1<<e)
    return value


def scan(carry,word):
    out = []
    for d in word:
        carry,v = column(carry,d)
        out.append(v)
    return carry,tuple(out)


def check_gap(word,g):
    r = sum(d%2 for d in word)
    f = reserve(word)
    (h,q),pword = scan((g,False),word)
    assert not q
    assert reserve(pword)-f == Fraction(g,1<<r)-h
    a = (h+1)//2
    tail = (2,)*(h%2)+(0,)*(a-h%2)
    extended = pword+tail
    assert reserve(extended)+a-f == Fraction(g,1<<r)


def check_danger(word):
    (z,passes),new = scan((0,True),word)
    assert z == 0
    dead = [i for i,d in enumerate(word) if d == 0]
    assert passes == (not dead)
    if passes:
        assert reserve(word)<1 and reserve(new)>=reserve(word)
        return
    stop = dead[0]
    ones_after = sum(d%2 for d in word[stop:])
    erased = [i for i in range(stop) if word[i]==1]
    delta = -Fraction(1,1<<(ones_after+1))
    for v,i in enumerate(erased,1):
        ones_from = sum(d%2 for d in word[i:])
        delta += Fraction((1<<(len(erased)-v))-1,1<<ones_from)
    assert reserve(new)-reserve(word) == delta >= Fraction(-1,2)


def first_gap_halts(word,g):
    """Test whether P^g followed by Q halts on this finite upper word."""
    r = c = 0
    for d in word:
        u,e = divmod(d,2)
        if not e and ((g+c)>>r)&1 != 1-u:
            return False
        c += (1-u)<<r
        r += e
    return g+c < 2<<r


def main():
    assert LIST[25] == M26 == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    checked = 0
    for n in range(6):
        for word in product(range(4),repeat=n):
            check_danger(word)
            for g in range(14):
                check_gap(word,g)
                (h,passes),_ = scan((g,True),word)
                assert first_gap_halts(word,g) == (passes and h <= 1)
                checked += 1
            if n <= 3:
                assert first_gap_halts(word,9) == (raw_tick(word) is None)
    print('signed P and Q accounting and closed halting test:',checked,'word/gap checks')
    for b in range(9):
        for g in range(600):
            assert first_gap_halts((3,)*b,g) == (g < 2<<b)
    print('all-one suffix threshold checked on 5400 cases')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
