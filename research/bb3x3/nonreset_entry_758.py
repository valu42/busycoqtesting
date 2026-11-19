#!/usr/bin/env python3
"""Verify an absorbing rectangle of ordinary counter states near the target mass."""
from check_bb33 import champion_step
from scale_clauses_758 import H
from target_basin_758 import GATES_NEW, NEAR, least_tail_margin, read_tails
from target_shadow_758 import C, D, POWER

FAR = GATES_NEW[20][1]
MIN_JUMPS = 251
MAX_CUT = 307 - MIN_JUMPS + 1
MAX_CALLS = 307 + 1 + 243 + 2
MAX_GAIN = 9*MAX_CALLS//2
MIN_MASS = H-FAR
MAX_MASS = H-NEAR-MAX_GAIN
MAX_H = 2*(MIN_MASS//(2*3**MIN_JUMPS))


def verify():
    assert MAX_CUT//2 == 28
    assert 0 < C < 594*D
    assert 3**MIN_JUMPS*MAX_H <= MIN_MASS
    assert 2*3**293 > MAX_MASS+2*293
    # U-u_aligned is positive and <= FAR+594 at every allowed mass.
    assert NEAR+MAX_GAIN > 2*292
    margin = FAR+2600
    assert min(3**MIN_JUMPS, 3**(307-MAX_CUT-188-2)) > D*margin
    listed_margin = least_tail_margin(read_tails(28))
    assert POWER*listed_margin > D*3**MAX_CUT*margin
    assert MAX_CALLS == 553 and MAX_GAIN == 2488
    # Replay physical corner and interior examples directly as a regression.
    us = {MIN_MASS + MIN_MASS%2, MAX_MASS - MAX_MASS%2,
          2*((MIN_MASS+MAX_MASS)//4)}
    hs = {2, 4, MAX_H, MAX_H-2, 2*(MAX_H//4)}
    for u in us:
        for h in hs:
            a,c = 2*h-1,u-h+1
            assert a%4 == 3 and c%2 and (a+2*c-1)//2 == u
            for calls in range(1, MAX_CALLS+1):
                state = champion_step(a,c)
                assert state is not None
                a,c = state
                if a==1:
                    break
            assert a==1 and H-FAR <= c <= H-NEAR and 0 < c-u <= MAX_GAIN
    masses = MAX_MASS//2 - (MIN_MASS-1)//2
    print(f'Even h from 2 through {MAX_H:,}, {masses:,} admissible even masses.')
    print(f'{masses*(MAX_H//2):,} ordinary states return to the halting basin within {MAX_CALLS} calls.')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('run without -O for verification')
    verify()
