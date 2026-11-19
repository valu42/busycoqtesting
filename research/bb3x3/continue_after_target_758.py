"""Search for a terminal after the common post-H checkpoint of #758."""
import argparse
from bisect import bisect_left, bisect_right

from after_target_758 import CHECKPOINT, EDGE, H
from check_bb33 import champion_step, first_return
from check_confluence import itinerary

POWER = 3**292
DISTANCE = 10**60
ODD_PREFIX = 'L'*8+'J'+'L'*4+'J'
PERIOD = 8192


def after_jumps(s):
    if s % 2:
        a,c = 2*POWER-1, s-POWER+585
    else:
        a,c = 4*(POWER//3)-1, s-2*(POWER//3)+587
    assert c > 0 and s > POWER
    return a,c


def launch(z, guards=False):
    """Ordinary prefix at the odd seed EDGE+z; extended without guards for residues."""
    assert z%2 == 0
    a,c = after_jumps(EDGE+z)
    for letter in ODD_PREFIX:
        if letter == 'J':
            if guards:
                assert a%2 == c%2 == 1 and a <= c and a>1
            a,c = 3*a+2,c-a+1
        else:
            q = (c+1)//4
            if guards:
                assert c%2 and a >= 4*q+3
            a,c = a-4*q-3,6*q+5
        if guards:
            assert a>1
    return (c+7)//2


def terminal_search():
    first = CHECKPOINT-EDGE
    ymax = launch(DISTANCE,True)
    ymin = launch(first+first%2,True)
    even = 'J'*291+'LLJLLJLR'
    for s in (CHECKPOINT,EDGE+DISTANCE-1):
        assert itinerary(s)[0] == even
    table = [launch(z) for z in range(0,PERIOD,2)]
    assert table == sorted(table)
    shift = 4_650_361
    assert all(launch(z+PERIOD) == table[z//2]+shift for z in range(0,PERIOD,2))
    # The right-counter coordinate after k bulks lies in [(3/2)^k y,
    # (3/2)^k(y+3)]. A terminal with empty suffix or initial J has slope >=2/9.
    assert 3**800*ymin > 2**800*(EDGE+DISTANCE+20_000)
    powers = [(2**k,3**k) for k in range(0,800,2)
              if 3**k*(ymax+3) > (EDGE//5)*2**k
              and 3**k*ymin < (EDGE+DISTANCE+20_000)*2**k]
    checked = set()
    words = 0

    def examine(a, b):
        nonlocal words
        words += 1
        # At the end of k initial bulks, |y' - (a/b)u'|<20.
        low = a*CHECKPOINT-20*b
        high = a*(EDGE+DISTANCE+20_000)+20*b
        for scale, numerator in powers:
            divisor = numerator*b
            start = max(ymin,scale*low//divisor-3)
            end = min(ymax,scale*high//divisor+1)
            if end < start:
                continue
            assert end-start < shift
            first_lift = (start-table[0])//shift
            for lift in (first_lift,first_lift+1):
                offset = lift*shift
                left = bisect_left(table,start-offset)
                right = bisect_right(table,end-offset)
                for idx in range(left,right):
                    z = lift*PERIOD+2*idx
                    if first <= z <= DISTANCE and z not in checked:
                        checked.add(z)
                        assert first_return(EDGE+z) is not None

    def inverse(a, b, calls, starts_with_pair):
        if not starts_with_pair:
            examine(a,b)
        if calls < 18:
            inverse(a+b,3*b,calls+1,False)
        if calls+2 <= 18:
            inverse(4*a,9*b,calls+2,True)

    inverse(2,9,0,False)
    assert (words,len(checked)) == (6765,4362)
    print('6,765 coarse suffixes, 4,362 candidate starts, no direct halt in this class.')


def bulk_table(n):
    table = []
    for residue in range(2**n):
        y,gain = residue,0
        for _ in range(n):
            gain += 5+4*(y%2)
            y = 3*((y+1)//2)
        table.append((y,gain))
    return table


def verify_trace():
    n = 14
    table = bulk_table(n)
    mask = (1<<n)-1
    factor = 3**n
    seed = CHECKPOINT
    elapsed = 0
    longest = 0
    for i in range(500_000):
        a,c = after_jumps(seed)
        calls = 292
        while True:
            if a >= 4*((c+1)//4)+3:
                y = (c+7)//2
                small, gain = table[y&mask]
                after_c = 2*((y>>n)*factor+small)-7
                after_a = a+2*(c-after_c)+gain
                if after_a >= 0:
                    a,c = after_a,after_c
                    calls += n
                else:
                    q = (c+1)//4
                    a,c = a-4*q-3,6*q+5
                    calls += 1
            else:
                next_state = champion_step(a,c)
                assert next_state is not None
                a,c = next_state
                calls += 1
            if a == 1:
                break
        if i<32 or i%8191 == 0:
            assert c == first_return(seed,batch=False)
        assert c > seed
        seed = c
        elapsed += calls
        longest = max(longest,calls)
    assert (seed-EDGE,elapsed,longest) == (1_256_970_693,420_169_510,1106)
    print('500,000 first returns from C use 420,169,510 calls and reach EDGE+1,256,970,693.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trace',action='store_true',help='also replay the conditional orbit from C')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions for the checks')
    terminal_search()
    if args.trace:
        verify_trace()
