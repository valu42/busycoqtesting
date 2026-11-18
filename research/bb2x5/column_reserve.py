"""Exact dyadic accounting for P gaps and for Q at aligned line-26 checkpoints."""
from fractions import Fraction
from itertools import product

from column_phases import lift, p_step, q_step
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


def danger_delta(u,e,stop):
    """Change of F for an ordinary Q with a zero tail and zero-based stop."""
    low = (1<<stop)-1
    erased = (~u)&low
    count = erased.bit_count()
    numerator = -(1<<(e&low).bit_count())
    while erased:
        bit = erased&-erased
        erased -= bit
        count -= 1
        prefix_ones = (e&(bit-1)).bit_count()
        numerator += 2*((1<<count)-1)*(1<<prefix_ones)
    return Fraction(numerator,2<<e.bit_count())


def check_common_clock(ticks):
    u = e = wraps = 0
    clock = Fraction(0)
    records = []
    decreasing = 0
    for tick in range(1,ticks+1):
        old_clock = clock
        for _ in range(9):
            u,depth = p_step(u,e)
            wraps += depth == 0
        clock += Fraction(9,1<<e.bit_count())
        new_e,depth = q_step(u,e)
        stop = depth-1
        assert stop >= 0
        for k in range(len(records),stop+1):
            gap = k+clock.numerator//clock.denominator
            assert (gap+1)//2 == wraps
            assert (wraps > 3+k) == (clock >= k+7)
            records.append((tick,gap,wraps))
        clock += danger_delta(u,e,stop)
        e = new_e
        decreasing += clock < old_clock
        # Fixed width strictly above the support emits exactly two Ps per wrap.
        length = max(u,e).bit_length()+1
        word = tuple(2*((u>>i)&1)+((e>>i)&1) for i in range(length))
        assert clock == 2*wraps+reserve(word)-length
    gaps = [9]
    for k in range(min(len(records),12)):
        assert records[k][1] == gaps[0]
        if k < 11:
            gaps = lift(gaps)
    print('common clock:', ticks,'ticks,',len(records),'first arrivals,',
          decreasing,'negative full-tick changes')
    print('selected (upper width, tick, leading gap, wraps):',
          [(k,*records[k]) for k in range(0,len(records),4)])


def variable_selector_loss(width):
    """Carry path from zero to a single high e bit, with freely chosen u."""
    e = 0
    loss = Fraction(0)

    def rise(k):
        nonlocal e,loss
        top = 1<<(k-1)
        assert not e&(2*top-1)
        if k > 1:
            rise(k-1)
        if k > 2:
            rise(k-2)
        # Select every existing one below the new stop, and the stop itself.
        u = (top-1)&~e
        next_e,depth = q_step(u,e)
        assert depth == k
        loss -= danger_delta(u,e,k-1)
        e = next_e
        assert (e&(2*top-1)) == top

    rise(width)
    assert e == 1<<(width-1)
    return loss


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
    check_common_clock(10000)
    losses = [variable_selector_loss(k) for k in range(1,17)]
    assert losses[:2] == [Fraction(1,2),1]
    for k in range(2,len(losses)):
        assert losses[k] == losses[k-1]+losses[k-2]/2+Fraction(1,4)
    print('freely chosen Q-selector loss at widths 1, 4, 8, 12, 16:',
          [str(losses[k-1]) for k in (1,4,8,12,16)])


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
