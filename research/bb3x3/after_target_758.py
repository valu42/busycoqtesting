"""Verify the common #758 continuation after the large halting target H."""
import argparse
from array import array
from collections import Counter
from heapq import heapify, heappop, heappush

from check_bb33 import HALTING_TARGET as H, champion_step, first_return
from check_confluence import itinerary

# The last odd seed in the first ordinary return corridor above H.
FAR_DISTANCE = int(
    "125934394113084012169643581938338954521469140621623562967699085766993849"
    "12683206137352573392212214398155200667315120427833161777739441912")
EDGE = H + FAR_DISTANCE
CHECKPOINT = EDGE + 7_784_831
BOUNDARY_SIZE = 3_403_055


def verify_corridor():
    """Verify both endpoints of each parity and their positive intermediate states."""
    even = 'J'*291+'LLJLLJLR'
    odd = 'J'*291+'LLLLLLLLJLLLLLR'
    for first, last, word, cap in ((H+1, EDGE-1, even, 615), (H+2, EDGE, odd, 647)):
        assert first % 2 == last % 2
        assert itinerary(first) == itinerary(last) == (word, 2*cap)
        state = champion_step(1, last)
        for _ in word[:-1]:
            assert state[0] > 1
            state = champion_step(*state)
        assert state[0] > 1 and champion_step(*state)[0] == 1
    assert itinerary(EDGE+2)[0] != odd
    # Use every potential overshoot; the propagation does not need a residue cycle.
    active = set(range(EDGE+1, EDGE+648))
    queue = list(active)
    heapify(queue)
    edges = 0
    while len(active) > 1:
        seed = heappop(queue)
        active.remove(seed)
        nxt = first_return(seed)
        assert nxt is not None and seed < nxt <= CHECKPOINT
        if nxt not in active:
            active.add(nxt)
            heappush(queue, nxt)
        edges += 1
    assert active == {CHECKPOINT} and edges == 14_216
    assert first_return(CHECKPOINT, batch=False) == EDGE+7_785_442
    print(f'{edges:,} distinct first returns merge all 647 exits at EDGE+7,784,831.')


def verify_boundary():
    """Classify every integer in the last 3,403,055 reset parameters through H."""
    outcomes = array('h', [0])*BOUNDARY_SIZE
    counts = Counter()
    largest_gain = 0
    for d in range(BOUNDARY_SIZE):
        seed = H-d
        nxt = first_return(seed)
        if d % 65_537 == 0 or d < 10:
            assert nxt == first_return(seed, batch=False)
        if nxt is None:
            assert d in (0,2)
            outcome = -1-d  # distinguish the two last reset parameters
        else:
            assert nxt > seed
            largest_gain = max(largest_gain, nxt-seed)
            outcome = outcomes[H-nxt] if nxt <= H else nxt-H
        outcomes[d] = outcome
        counts[outcome] += 1
    exits = [x for x in counts if x > 0]
    assert (len(exits),min(exits),max(exits),largest_gain) == (346,2,1243,1409)
    assert counts[-1] == 2_238_030 and counts[-3] == 2_511
    assert sum(counts[x] for x in exits) == 1_162_514
    assert sum(counts.values()) == BOUNDARY_SIZE
    print('2,238,030 starts halt via H, 2,511 via H-2, and 1,162,514 cross alive.')


def verify_escape():
    """Apply the exceptional annulus and determinant bounds at this new mass."""
    d,r = 0,1
    for _ in range(785):
        q = (r+1)//4
        d,r = d+4*q+3, 6*q+5
    lower,upper = 2*(H+1)+1, 2*EDGE+1-5458
    assert d-6 <= lower <= upper < upper+5458 <= d+r-6
    # Entry can overshoot the threshold by eight; discard partial end blocks.
    calls = (upper-(lower+8)+8)//9
    blocks = (calls-2)//2
    factors = 3*10**67
    n = 577
    assert blocks >= factors**2+n+2
    assert 3**n > 9*factors**2*(EDGE+10)
    print(f'A live passage missing the common checkpoint needs {factors} length-{n+1} factors.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boundary', action='store_true', help='also classify all 3,403,055 starts below H')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with verification assertions enabled')
    verify_corridor()
    verify_escape()
    if args.boundary:
        verify_boundary()
