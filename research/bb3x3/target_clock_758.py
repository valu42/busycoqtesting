"""Conditional raw clocks for approaches to the #758 halting reset and its bypass."""
import argparse
from bisect import bisect_right
from collections import Counter
from functools import cache
from math import comb

from after_target_758 import BOUNDARY_SIZE, CHECKPOINT, EDGE, H, verify_corridor
from check_bb33 import POWERS_OF_THREE, champion_step, first_return
from timing_758 import branch_cost

MODULUS = 1 << 14
ORIGIN = H+1


def timed_return(seed, batch=True):
    """Run one first return, including the terminal call if the segment halts."""
    a, c, elapsed = 1, seed, 0
    while True:
        if batch and a % 2 and c % 2 and c > 8*a:
            u = a+1
            mass = a+2*c
            k = bisect_right(POWERS_OF_THREE, (2*c+u)//u)-1
            power = POWERS_OF_THREE[k]
            twice = (6*u*u*((power*power-1)//8)-17*u*((power-1)//2)
                     + k*(23+5*mass)+10*k*(k-1))
            assert twice % 2 == 0
            elapsed += twice//2
            a, c = u*power-1, c-u*((power-1)//2)+2*k
        else:
            elapsed += branch_cost(a,c)
            state = champion_step(a,c)
            if state is None:
                return None,elapsed
            a,c = state
        if a == 1:
            assert c > seed
            return c,elapsed


@cache
def polynomial(residue,origin,modulus):
    seed = origin+residue
    samples = [timed_return(seed+j*modulus) for j in range(4)]
    gain = samples[0][0]-seed
    assert all(nxt == seed+j*modulus+gain for j,(nxt,_) in enumerate(samples))
    a,b,c,d = (dt for _,dt in samples)
    second = c-2*b+a
    assert d-2*c+b == second
    return gain,a,b-a,second


def evaluate(seed,origin=ORIGIN,modulus=MODULUS):
    q,residue = divmod(seed-origin,modulus)
    gain,a,b,c = polynomial(residue,origin,modulus)
    return seed+gain,a+b*q+c*comb(q,2)


def cycle_cost(seed,length,stride,origin,modulus):
    initial = seed
    elapsed = 0
    for _ in range(length):
        seed,delta = evaluate(seed,origin,modulus)
        elapsed += delta
    assert seed == initial+stride
    return elapsed


@cache
def first_pass(seed,origin=ORIGIN,edge=EDGE,modulus=MODULUS,max_gain=647):
    count = clock = 0
    seen = {}
    while seed <= edge:
        residue = (seed-origin) % modulus
        if residue in seen:
            old,index = seen[residue]
            stride,length = seed-old,count-index
            copies = (edge-seed)//stride
            if copies >= 4:
                a,b,c,d = [cycle_cost(seed+j*stride,length,stride,origin,modulus) for j in range(4)]
                second = c-2*b+a
                assert d-2*c+b == second
                clock += copies*a+comb(copies,2)*(b-a)+comb(copies,3)*second
                seed += copies*stride
                count += copies*length
            seen.clear()
        seen[residue] = seed,count
        seed,delta = evaluate(seed,origin,modulus)
        count += 1
        clock += delta
    assert seed <= edge+max_gain
    return seed,count,clock


def follow(seed, known, limit):
    """Follow a path to a cached outcome. Cache the elapsed time for each suffix."""
    path = []
    while seed not in known:
        assert seed is not None and seed <= limit
        nxt,delta = timed_return(seed)
        path.append((seed,delta))
        seed = nxt
    count,clock = known[seed]
    for seed,delta in reversed(path):
        count += 1
        clock += delta
        known[seed] = count,clock
    return count,clock


def verify_boundary_clocks(escape):
    # Next reset always advances by at most 1,409 within the classified boundary.
    # A circular array keeps the complete future needed by the induction.
    ring = [None]*1410
    counts = Counter()
    extrema = {}
    for distance in range(BOUNDARY_SIZE):
        seed = H-distance
        nxt,clock = timed_return(seed)
        if nxt is None:
            assert distance in (0,2)
            outcome,count = distance,1
        elif nxt <= H:
            assert 0 < nxt-seed < len(ring)
            outcome,count,delta = ring[(H-nxt) % len(ring)]
            clock += delta
            count += 1
        else:
            assert 0 < nxt-seed < len(ring)
            delta,offset,n,_ = escape[nxt]
            assert offset == nxt-H
            outcome,count,clock = -1,n+1,clock+delta
        ring[distance % len(ring)] = outcome,count,clock
        row = clock,distance,count
        counts[outcome] += 1
        low,high = extrema.get(outcome,(row,row))
        extrema[outcome] = min(low,row),max(high,row)
    assert counts == {0:2_238_030,2:2_511,-1:1_162_514}
    expected_offsets = {0:(0,3_402_774),2:(2,52_583),-1:(288,3_403_054)}
    for outcome,(low,high) in extrema.items():
        assert (low[1],high[1]) == expected_offsets[outcome]
        print('last reset offset',outcome,'number of starts',counts[outcome],
              'min and max (time, starting distance, segments)',low,high)
    assert extrema[0][1][0]//10**271 == 1254206229300
    assert extrema[2][1][0]//10**269 == 1959606359561
    low,high = extrema[-1]
    assert low[0]//10**284 == high[0]//10**284
    assert low[0]//10**283 != high[0]//10**283


def verify(boundary=False):
    verify_corridor()
    for seed in [*range(1,257),H-12_000_000,H-2,H,H+1,H+2,EDGE,EDGE+1,CHECKPOINT]:
        assert timed_return(seed) == timed_return(seed,batch=False)

    halt_suffix = {None:(0,0)}
    for seed in (H-12_000_000,H-3_403_055,H,H-2):
        count,clock = follow(seed,halt_suffix,H)
        print('Halting start H',seed-H,'segments',count,'clock',clock,flush=True)

    # The exhaustive boundary verification bounds each single reset gain by 1,409.
    exits = set()
    for offset in range(1409):
        nxt = first_return(H-offset)
        if nxt is not None and nxt > H:
            exits.add(nxt)
    assert (len(exits),min(exits)-H,max(exits)-H) == (346,2,1243)
    post_suffix = {CHECKPOINT:(0,0)}
    timings = []
    for seed in sorted(exits):
        crossing,count,clock = first_pass(seed)
        n,t = follow(crossing,post_suffix,CHECKPOINT)
        timings.append((clock+t,seed-H,count+n,crossing-EDGE))
    assert min(timings)[1] == 906 and max(timings)[1] == 62
    assert len({x[-1] for x in timings}) == 30
    assert min(timings)[0]//10**397 == max(timings)[0]//10**397 == 5206702307543299
    # Compare polynomial evaluation against original scalar rules far from its samples.
    for offset in range(1,647,17):
        seed = EDGE-offset
        assert evaluate(seed) == timed_return(seed,batch=False)
    for description,row in [('minimum',min(timings)),('maximum',max(timings))]:
        print(description,'raw clock, initial offset, first returns, exit offset',*row)
    print('distinct far-edge exits',len({x[-1] for x in timings}))
    if boundary:
        verify_boundary_clocks({H+row[1]:row for row in timings})


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O so verification checks execute.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boundary',action='store_true',
                        help='audit all 3,403,055 boundary starts and their clocks')
    verify(parser.parse_args().boundary)
