"""Localize origins of any live excursion skipping the halting basin after 3^292."""
import argparse
from decimal import Decimal

from check_bb33 import HALTING_TARGET as H, champion_step
from power_approach_758 import CHECKPOINT as START, EXPONENT, POWER

BASIN_LOW = H-33_533_929_283_358
BASIN_HIGH = H-3_403_055
END = BASIN_LOW-1
DEPTH = 23


def launch(seed):
    if seed % 2:
        return 2*POWER-1,seed-POWER+1+2*EXPONENT,4*EXPONENT
    third = POWER//3
    return 4*third-1,seed+2*EXPONENT+3-2*third,8+4*(EXPONENT-1)


def signature(seed):
    a,c,cost = launch(seed)
    word = bytearray()
    for _ in range(2000):
        q = (c+1)//4
        if a >= 4*q+3:
            a,c = a-4*q-3,6*q+5
            word.append(1)
            cost += 9
        elif a % 2 == 0:
            # An even-left terminal call here halts or returns. A return charges five.
            return bytes(word),(cost+5)//2
        elif a <= c:
            a,c = 3*a+2,c-a+1
            word.append(2)
            cost += 4
        else:
            break
    return None,0


def check_launch(seed):
    state = 1,seed
    for _ in range(EXPONENT):
        a,c = state
        assert a <= c and a%2
        state = champion_step(a,c)
    a,c,cost = launch(seed)
    assert state == (a,c) and a+2*c-(1+2*seed) == cost


def classify(parity,depth,bands):
    low = START+(parity-START)%2
    high = END-(END-parity)%2
    check_launch(low)
    check_launch(high)
    pending = [(low,high,0)]
    unresolved = []
    cap = covered = boxes = 0
    while pending:
        first,last,d = pending.pop()
        pattern,gain = signature(first)
        other,_ = signature(last)
        if pattern is not None and pattern == other:
            covered += (last-first)//2+1
            cap = max(cap,gain)
        elif d < depth:
            mid = first+2*((last-first)//4)
            pending.append((mid+2,last,d+1))
            pending.append((first,mid,d+1))
        else:
            boxes += 1
            if unresolved and unresolved[-1][1]+2 == first:
                unresolved[-1][1] = last
            else:
                unresolved.append([first,last])
    total = (high-low)//2+1
    missed = sum((b-a)//2+1 for a,b in unresolved)
    assert covered+missed == total and END+cap <= BASIN_HIGH
    largest = max(b-a+2 for a,b in unresolved)
    if depth == DEPTH:
        assert (boxes,len(unresolved),cap) == ((134_524,27_525,768),(171_521,35_042,780))[parity]
        assert largest*10**9 < 1073*(END-START)
        assert 100000*missed < (1604,2045)[parity]*total
        if parity == 0:
            assert 1000000*(H-unresolved[-1][1]) > 2291*H
    if bands is not None:
        for a,b in unresolved:
            print(parity,a,b,file=bands)
    print('parity',parity,'unresolved spans',len(unresolved),'max certified gain',cap,
          'covered',covered,'total',total,'fraction covered',Decimal(covered)/Decimal(total))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--depth',type=int,default=DEPTH)
    parser.add_argument('--bands',type=argparse.FileType('w'),
                        help='write parity, first and last for every remaining span')
    args = parser.parse_args()
    if not __debug__ or not 1 <= args.depth <= 30:
        parser.error('enable assertions and use a depth from 1 through 30')
    for parity in (0,1):
        classify(parity,args.depth,args.bands)
