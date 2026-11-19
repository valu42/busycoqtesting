"""An amortized upper clock for BB(3,3) holdouts #758 and #153."""
from bisect import bisect_right
from decimal import Decimal
from fractions import Fraction
from itertools import pairwise

from check_bb33 import HALTING_TARGET, champion_step
from timing_758 import branch_cost


F = Fraction
RATE = F(33, 1058)
# Abscissas are in units of 1/23 and heights in units of 1/146004.
TABLE = (
    ((0, 0), (1, 5913), (2, 11101), (4, 20833), (5, 25285),
     (13, 24985), (15, 22801), (23, -37490)),  # odd left coordinate
    ((0, -713), (8, 27055), (10, 30751), (11, 32323), (23, -14720)),  # even
)
KNOTS = tuple(tuple(F(k,23) for k,_ in row) for row in TABLE)
HEIGHTS = tuple(tuple(F(v,146004) for _,v in row) for row in TABLE)


def potential(phase, x):
    knots = KNOTS[phase]
    ys = HEIGHTS[phase]
    i = min(bisect_right(knots,x)-1, len(knots)-2)
    assert 0 <= x <= 1 and i >= 0
    return ys[i] + (ys[i+1]-ys[i])*(x-knots[i])/(knots[i+1]-knots[i])


def reward(x):
    return 3*min(x,(1-x)/2)**2


def certify_potential():
    """Every displayed homogeneous inequality is convex between breakpoints."""
    third = F(1,3)
    branches = (
        (0,0,0,third,3,0,4),                    # J
        (0,1,third,1,F(3,2),F(-1,2),5),        # odd-left bulk
        (1,0,third,1,F(3,2),F(-1,2),5),        # even-left bulk
        (1,0,0,third,0,0,5),                    # R
        (0,0,third,third,0,1,8),                # E boundary
    )
    worst = 0
    for phase, knots in enumerate(KNOTS):
        heights = HEIGHTS[phase]
        assert all(-F(1,2) <= v <= F(1,2) for v in heights)
        assert all(abs(b-a) <= 2*(hi-lo)
                   for (a,b),(lo,hi) in zip(pairwise(heights),pairwise(knots)))
    for first,last,lo,hi,slope,offset,gain in branches:
        breaks = {F(lo),F(hi),*KNOTS[first]}
        if slope:
            breaks.update((u-offset)/slope for u in KNOTS[last])
        for x in breaks:
            if lo <= x <= hi:
                y = slope*x+offset
                ratio = (reward(x)+potential(last,y)-potential(first,x))/gain
                worst = max(worst,ratio)
    assert worst == RATE
    # Independent equality witness in the relaxed continuum map.
    xs = [F(j,23) for j in (5,15,11)]
    assert sum(map(reward,xs))/(4+5+5) == RATE


def upper_prefix(v):
    """Upper clock from blank to an attained live map configuration of mass v."""
    assert v >= 2
    return 2 + 11*v**3//1058 + 8*v*v + 17*v


def terminal_suffix(seed):
    state = (1,seed)
    cost = 0
    for call in range(1,308):
        cost += branch_cost(*state)
        state = champion_step(*state)
        if state is None:
            assert call == 307
            return cost
    raise AssertionError('expected terminal at call 307')


def audit():
    certify_potential()
    for c in range(1,64):
        for a in range(64):
            if a != 1 and c%2 == 0:
                continue
            w = a+2*c
            t = branch_cost(a,c)
            x = F(a,w)
            assert t <= w*w*reward(x)+30*w+65
            target = champion_step(a,c)
            if target is None:
                continue
            na,nc = target
            nw = na+2*nc
            delta = potential(int(na%2==0),F(na,nw))-potential(int(a%2==0),x)
            assert w*w*(reward(x)+delta) <= RATE*(nw-w)*w*w+26*w
    a,c,raw = 0,1,2
    for _ in range(10_000):
        raw += branch_cost(a,c)
        a,c = champion_step(a,c)
        assert raw <= upper_prefix(a+2*c)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Enable verification assertions.")
    audit()
    for seed in (HALTING_TARGET-2, HALTING_TARGET):
        bound = upper_prefix(2*seed+1)+terminal_suffix(seed)
        assert bound < 8206*10**413
        print(f'If blank reaches H{seed-HALTING_TARGET:+d}, its raw halting clock '
              f'is at most {Decimal(bound):.12E} (rounded display).')
