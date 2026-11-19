"""Check 72,680 two-jump subintervals of the secondary cusp and emit merger inputs."""
import argparse
from functools import cache
from pathlib import Path

from power_cusp_758 import BITS, FACTOR, TABLE
from secondary_cusp_758 import H, Y, build_lanes, gate_rows


@cache
def bounds(total):
    """Sufficient inclusive edge offsets for this number of postheader bulks."""
    num, den = 3**total, 2**total
    low = -(-((2*H+20_000)*den+6_000*num)//(672*num))
    high = ((2*Y-4)*den-4_000*num)//(450*num)
    return max(64,low),high


def bulk_run(a,c,length):
    """Formal consecutive bulks, using the tabulated mass gain and right output."""
    y = (c+7)//2
    gain = 0
    for _ in range(length//BITS):
        high,low = divmod(y,1 << BITS)
        new_low,delta = TABLE[low]
        y,gain = high*FACTOR+new_low,gain+delta
    for _ in range(length%BITS):
        gain += 5+4*(y%2)
        y = 3*((y+1)//2)
    new_c = 2*y-7
    return a+2*(c-new_c)+gain,new_c


def witness(lanes,seed,first,second):
    """Check the full truncated word at one odd endpoint using integer counters."""
    periods,r = divmod(seed-Y,512)
    assert not r%2
    u,d = lanes[r//2]
    u += 512*periods
    d += 19_171*periods
    a,c = bulk_run(2*u-4*d-1,2*d+1,first)
    # A positive ending left counter certifies all proposed bulk decrements.
    assert a%2 and 1 < a <= c
    a,c = 3*a+2,c-a+1
    a,c = bulk_run(a,c,second)
    assert a%2 == 0 and 1 < a <= c


def bands():
    rows = gate_rows()
    for i,(k,_,edge) in enumerate(rows):
        first = k-1
        gap_end = rows[i-1][1]-1 if i else H
        cap = min(gap_end-edge,Y*2**first//(320*3**first)-8)
        previous = edge
        for total in range(799,k-1,-2):
            low,high = bounds(total)
            high = min(high,cap)
            if low <= high:
                assert previous < edge+low
                previous = edge+high
                yield k,edge,total,low,high


def verify(emit=False):
    # Largest ratio between the upper and lower bound on the second stopping
    # depth, attained at z=64. Three powers of 3/2 span a factor of 9/4.
    assert 6*(2*H+20_000)*(225*64+2_000) < 9*(2*Y-4)*(224*64-2_000)
    assert 7*3**800 > (H+10_000)*2**800
    lanes = build_lanes()
    count = width = 0
    connected = []
    for k,edge,total,low,high in bands():
        for z in (low+low%2,high-high%2):
            if low <= z <= high:
                witness(lanes,edge+z,k-1,total-k+1)
        count += 1
        width += high-low+1
        if total == 733 and (low,high) == (53_719_288,80_126_735):
            connected.append((k,edge))
    assert count == 72_680
    assert 10**9*width//(H-Y) == 236_655_081
    old_width = sum(hi-lo for _,lo,hi in gate_rows())
    assert 10**9*(old_width+width)//(H-Y) == 636_546_757
    assert [k for k,_ in connected] == list(range(7,734,2))
    if emit:
        path = Path(__file__).with_name('checkpoint_y_census_758.tsv')
        with path.open() as source:
            previous = {k:z for k,_,_,z in (map(int,line.split()) for line in source)}
        for k,edge in connected:
            print(k,edge,previous[k])
    else:
        print(f'{count:,} disjoint intervals. Together with the original corridors they cover '
              f'{100*(width+old_width)/(H-Y):.8f}% of the Y-to-H seed range.')
        print(f'The 733-bulk interval is present beyond {len(connected)} original mergers.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--merger-input',action='store_true',help='emit the input to checkpoint_y --edge-bands')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    verify(args.merger_input)
