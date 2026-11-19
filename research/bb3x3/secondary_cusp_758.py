"""Locate the pure bulk corridors after the last annular checkpoint."""
from functools import lru_cache

from annular_skip_758 import openings, replay
from check_bb33 import HALTING_TARGET as H
from check_confluence import itinerary
from power_cusp_758 import BITS, FACTOR, TABLE

P = 3**292
Y = 3**301//19_171 + 4_510_976
HEADER = 'L'*8+'J'
G = 10**10*3**264


def literal_header(seed):
    a,c = replay(openings(seed),HEADER,seed)
    return (a+2*c-1)//2,(c-1)//2


def verify():
    assert H%2 == Y%2 == 1
    for s in (Y,H):
        assert openings(s).k == 292
        a,c = replay(openings(s),HEADER+'LLLL',s)
        assert a>1 and c>0

    lanes = [literal_header(Y+2*i) for i in range(256)]
    beta = [512*d-19_171*2*i for i,(_,d) in enumerate(lanes)]
    gains = [u-Y-2*i for i,(u,_) in enumerate(lanes)]
    assert (min(beta),max(beta),min(gains),max(gains)) == (86_491_247_812,86_491_353_110,606,622)
    for i,(u,d) in enumerate(lanes):
        assert literal_header(Y+2*i+512) == (u+512,d+19_171)

    def edges(k):
        @lru_cache(None)
        def bulk(i):
            lane_u,lane_d = lanes[i%256]
            u,d = lane_u+512*(i//256),lane_d+19_171*(i//256)
            a,c = 2*u-4*d-1,2*d+1
            y,gain = (c+7)//2,0
            for _ in range(k//BITS):
                high,low = divmod(y,1<<BITS)
                small,g = TABLE[low]
                y,gain = high*FACTOR+small,gain+g
            for _ in range(k%BITS):
                gain += 5+4*(y%2)
                y = 3*((y+1)//2)
            nc = 2*y-7
            return a+2*(c-nc)+gain,nc

        def first(predicate):
            lo,hi = -1,(H-Y)//2+1
            while lo+1 < hi:
                mid = (lo+hi)//2
                if predicate(*bulk(mid)):
                    hi = mid
                else:
                    lo = mid
            return Y+2*hi

        return first(lambda a,c: a<=c),first(lambda a,c: a<0)

    rows = [(k,*edges(k)) for k in range(7,742,2)]
    assert all(Y<lo<hi<H for _,lo,hi in rows)
    assert all(rows[i+1][2]<rows[i][1] for i in range(len(rows)-1))
    assert edges(5) == (H+2,H+2) and edges(743) == (Y,Y)
    for k,lo,hi in rows:
        pattern = 'J'*292+HEADER+'L'*k+'R'
        for s,valid in ((lo-2,False),(lo,True),(hi-2,True),(hi,False)):
            assert ('J'+itinerary(s)[0] == pattern) == valid
    width = sum(hi-lo for _,lo,hi in rows)
    gap = rows[0][1]-rows[1][2]
    assert 10**9*width//(H-Y) == 399_891_676
    assert 408_284_364 < 10**9*gap//G < 408_284_366
    assert (rows[-1][1]-Y,rows[-1][2]-Y) == (1_750_734,4_881_882)
    print(len(rows),'corridors; combined width',width)
    print('gap between lengths nine and seven',gap)
    print('closest corridor to Y',rows[-1][1]-Y,rows[-1][2]-Y)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    verify()
