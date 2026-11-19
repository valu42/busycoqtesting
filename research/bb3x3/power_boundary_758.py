"""Advance through the change of word at a power of three or its double."""
from collections import Counter
from fractions import Fraction

from check_bb33 import champion_step
from power_gates_758 import coarse_return, gate_exits
from power_skip_758 import MIN_EXPONENT, margins, skip
from target_clock_758 import timed_return
from timing_758 import branch_cost


def certify_guards():
    """Affine margin proof for the parity which keeps its word across each cut."""
    p = 3**MIN_EXPONENT
    assert 2*MIN_EXPONENT+11 <= p//1000 and 1000 <= p//1000
    assert 8*(MIN_EXPONENT+12)*3**MIN_EXPONENT < 4**MIN_EXPONENT
    for multiple in (1, 2):
        even = multiple == 1
        for side in (-1, 1):
            slope = multiple + Fraction(side, 1000)
            a = margins(p, slope*p, multiple, even)
            b = margins(p+1, slope*(p+1), multiple, even)
            assert all(y >= x > 0 for x,y in zip(a,b))


def departure(m, multiple, offset):
    """Launch state after the first changed word, from the parity-specific exit."""
    p = 3**m
    if multiple == 1:
        assert 2 <= offset <= 4*m+34 and offset%2 == 0
        return 2*p-1, max(1,offset-3)
    assert multiple == 2 and 2 <= offset <= 4*m+16 and offset%2 == 0
    return 4*p-1, offset-1


def cut(m, multiple):
    return multiple*3**m - 2*m - (4 if multiple == 1 else 6)


def raw_launch(m, multiple, offset):
    """Verify and time the exact m or m+1 calls before the first bulk."""
    a,c = 1,cut(m,multiple)+offset
    raw = 0
    for _ in range(m+(multiple==2)):
        raw += branch_cost(a,c)
        a,c = champion_step(a,c)
        assert a != 1
    assert (a,c) == departure(m,multiple,offset)
    return raw


def maximal_bulks(m, multiple, offset):
    a,c = departure(m,multiple,offset)
    x = (c+1)//4+3
    raw = count = 0
    while a >= 4*x-9:
        raw += branch_cost(a,c)
        a,c = a-4*x+9, 6*x-13
        x = 3*x//2
        count += 1
    assert x == (c+1)//4+3 and 2*m <= count < 3*m
    return (a,c), count, raw


def event(state):
    a,c = state
    if a == 1:
        return 'at reset'
    if a <= c:
        return 'jump' if a%2 else 'return'
    return 'exceptional' if a%2 else 'halt'


def cross(m, multiple, start=None):
    """From the power corridor to the exact input of the first nonbulk call."""
    seed,returns,raw,_ = skip(m,multiple,start)
    edge = cut(m,multiple)
    extras = 0
    while seed <= edge or seed%2 != multiple%2:
        assert seed <= edge+(2*m+9) and extras < 26
        nxt,dt = timed_return(seed)
        assert nxt == coarse_return(m,seed,multiple)
        assert 2*m+3 <= nxt-seed <= 2*m+29
        seed = nxt
        raw += dt
        extras += 1
    offset = seed-edge
    state,bulks,dt = maximal_bulks(m,multiple,offset)
    raw += raw_launch(m,multiple,offset)+dt
    # 'returns' counts completed first returns through the departure reset.
    return offset, returns+extras, bulks, state, raw


def audit():
    certify_guards()
    for m in (20,34,292,1000):
        for multiple in (1,2):
            edge = cut(m,multiple)
            # Include endpoints, seam coalescence, and the parity's longest exit.
            cap = 4*m + (34 if multiple == 1 else 16)
            for e in (2,4,6,cap-2,cap):
                raw_launch(m,multiple,e)
                a,c = departure(m,multiple,e)
                state,n,clock = maximal_bulks(m,multiple,e)
                raw = 0
                for _ in range(n):
                    assert a >= 4*((c+1)//4)+3
                    raw += branch_cost(a,c)
                    a,c = champion_step(a,c)
                assert (a,c) == state and raw == clock and a < 4*((c+1)//4)+3
            offset,_,n,state,_ = cross(m,multiple)
            assert state == maximal_bulks(m,multiple,offset)[0]
            if m == 292:
                exits = gate_exits(m,multiple)
                outcomes = Counter(event(maximal_bulks(m,multiple,s-edge)[0]) for s in exits)
                print(f'At {multiple}*3**{m}, {len(exits)} candidate exits: {dict(outcomes)}.')
            print(f'm={m}, multiple={multiple}, departure offset={offset}, '
                  f'bulk calls={n}, next event={event(state)}.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    audit()
