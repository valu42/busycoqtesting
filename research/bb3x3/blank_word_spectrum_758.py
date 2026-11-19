"""Certify distinct complete return words sampled by the BB(3,3) blank orbit."""
import argparse
from fractions import Fraction as F
from math import comb, ceil, floor
from pathlib import Path

from check_bb33 import HALTING_TARGET, first_return
from scale_clauses_758 import check_word

GUARD_CLEARANCE = 20
COVERED_WIDTH = 100_090


def word_count(scale, inverse_length, max_direction, padding=GUARD_CLEARANCE):
    """Return the total, full binary depth, and greatest certified depth.

    A fixed initial word maps [0,1] to a cylinder of width inverse_length.
    In x=scale/t, a core width y costs at least scale*y/max_direction**2
    seed units. The two extremes of the middle gap lose padding/scale each.
    """
    total, full, highest = 0, -1, -1
    n = 0
    while True:
        count = 0
        for p in range(n+1):
            contraction = F(4**p, 3**(n+p))
            gap = F(2,9)*inverse_length*contraction
            width = (scale*gap-2*padding)/max_direction**2
            if width > COVERED_WIDTH:
                count += comb(n,p)
        if not count:
            return total, full, highest
        total += count
        if count == 2**n:
            full = n
        highest = n
        n += 1


def inspect(m, lo, hi):
    scale = 3**m
    xmin, xmax = F(5,9), F(19,27)
    low = ceil(scale/(xmax-F(GUARD_CLEARANCE,scale))-2*m)
    high = floor(scale/(xmin+F(GUARD_CLEARANCE,scale))-2*m)
    assert lo <= low <= high <= hi
    assert 100_000+2*m+9+2 < COVERED_WIDTH
    for s in (low+low%2, high-high%2):
        gain = check_word(s,'I'+'J'*(m-1)+'LR')
        assert gain in (2*m+7,2*m+9) and (s+gain)%2
    expected = {34:(30_968_802,21,28),35:(69_592_589,22,29)}[m]
    assert word_count(scale,F(4,27),xmax) == expected
    print(f'Exponent {m}: {expected[0]:,} distinct odd-reset words, '
          f'all words through {expected[1]} blocks, longest counted {expected[2]}.')


def doubled34():
    from check_fifth_power_bridge_758 import CUTS, HERE, read_rows
    rows = read_rows(HERE/'fifth_power_bridge_758.tsv')
    assert set(rows) == set(range(len(CUTS)-1))
    scale = 2*3**34
    for prefix,expected in (('PPPJ',(11_154_004,19,26)),('PPJPP',(6_675_699,19,25))):
        xmin,xmax = F(0),F(1)
        for letter in reversed(prefix):
            if letter == 'J':
                xmin,xmax = xmin/3,xmax/3
            else:
                xmin,xmax = (4*xmin+5)/9,(4*xmax+5)/9
        low = floor(scale/xmax)-72
        high = ceil(scale/xmin)-72
        assert CUTS[0] <= low < high <= CUTS[-1]
        for seed in (low+(1-low)%2,high-(high-1)%2):
            assert check_word(seed,'J'*34+'LR') in (73,75)
        assert word_count(scale,xmax-xmin,xmax) == expected
        # Check the opening and terminal on a representative even seed.
        x = xmin+F(4,9)*(xmax-xmin)
        seed = floor(scale/x)-72
        seed -= seed%2
        assert check_word(seed,'I'+'J'*34+prefix.replace('P','LL')+'LR') > 0
        print(f'Doubled exponent 34, prefix {prefix}: {expected[0]:,} different even-reset words.')


def target():
    p = 3**292
    r = F(4,9)**8
    low,high = p-584,ceil(p/(1-r))-584
    assert high+5_000 < HALTING_TARGET-53_463_914_736_831_321_850
    for s in (low+low%2,high-high%2):
        gain=check_word(s,'I'+'J'*291+'LLJLLLR')
        assert 0 < gain <= 615 and gain%2
    # delta>8/11 by the two strict rational bounds 0.449 and 0.551.
    assert 449**11*3**8 < 1000**11 and 551**11*9**8 < 1000**11*4**8
    epsilon=F(1,10**110)
    n=1
    while F(4,9)**n > epsilon:
        n+=1
    gain=9*(292+16+2*n+2)//2
    width=p*r*F(2,27)*epsilon-2*GUARD_CLEARANCE
    assert width>(10**21+3)*gain+3
    assert 110*8==80*11 and gain>=615
    assert 2*(width-630)-18 > 9*5*10**24
    print(f'Target-scale construction: >10^80 word intervals; '
          f'each width >{int(width):,} with at least 10^21 preceding true returns.')


def sample(m):
    scale=3**m
    for suffix in ('','J'*21,'P'*21,'JP'*10+'P'):
        lo,hi=F(1,3),F(5,9)
        for letter in reversed('PJ'+suffix):
            if letter=='J':
                lo,hi=lo/3,hi/3
            else:
                lo,hi=(4*lo+5)/9,(4*hi+5)/9
        near=scale/(hi-F(20,scale))-2*m
        far=scale/(lo+F(20,scale))-2*m
        assert far-near>COVERED_WIDTH
        for arrival in [floor(near)+1,ceil(far)-82]:
            # Any even entrance converts to odd without leaving the region.
            s=first_return(arrival) if arrival%2==0 else arrival
            assert s and s%2 and near<s<far
            letters=('PJ'+suffix).replace('P','LL')
            assert check_word(s,'J'*m+letters+'LR')>0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--power35-table',type=Path,help='also verify coverage of the exponent-35 word interval')
    args=parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    from check_double34_758 import rows
    verified=rows()
    inspect(34,verified[0][0],verified[-1][1])
    sample(34)
    doubled34()
    if args.power35_table is not None:
        from double35_frontier_758 import CUTS,read_table
        archive=read_table(args.power35_table)
        assert all(i in archive for i in range(len(CUTS)-1))
        inspect(35,CUTS[0],CUTS[-1])
        sample(35)
    target()
