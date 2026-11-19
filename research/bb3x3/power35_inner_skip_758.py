"""Verify a timed segment of the real blank orbit between powers 3^35 and 2*3^35."""
import argparse
from pathlib import Path
import subprocess

from annular_skip_758 import openings, replay
from check_bb33 import HALTING_TARGET
from double35_frontier_758 import CUTS, TABLE, read_table
from fifth_blank_clock_758 import timed_extension
from next_gate_after_fifth_758 import GOAL
from power_gates_758 import coalesce
from target_clock_758 import first_pass, timed_return

APPROACH = (50_881_545_099_034_461, 50_885_978_668_475_620,
            50_885_978_668_475_621, 50_885_978_668_475_787, 266_889, 486_725_045)
SOURCE = 50_885_978_668_530_449
ODD_START = 50_885_978_668_575_677
ODD_LAST = 50_885_984_713_694_621
EVEN_START = 50_885_984_713_696_064
EVEN_LAST = 51_054_820_342_878_382
DESTINATION = 51_054_820_342_885_124
PREVIOUS_CLOCK = (
    1_482_784_176_152_518_686_967_781_313_684_540_616_202_754_440_890,
    1_988_454_072_317_701_732_753_123_726_748_110_537_604_032_294_736,
)
DESTINATION_CLOCK = (
    1_581_817_673_027_642_920_548_815_318_052_885_252_113_873_545_030,
    2_176_662_525_994_515_438_813_642_824_555_902_900_721_567_866_334,
)
DURATION = 26_657_304_251_347_328_769_027_871_467_526_286_778_627_812_518


def certify_word(low, high, word):
    """Check every guard over an entire fixed-parity interval by endpoint order."""
    assert (high-low)%2 == 0 and low <= high
    launch = openings(low)
    assert openings(high) == launch
    left,right = launch.state(low),launch.state(high)
    for i,op in enumerate(word):
        assert left[0] >= right[0] > 1 and left[1] <= right[1]
        assert left[0]%2 == right[0]%2
        for a,c in (left,right):
            if op == 'L':
                assert a >= 4*((c+1)//4)+3
            else:
                assert op == 'J' and a%2 and a <= c
        left,right = (replay(launch,word[:i+1],s) for s in (low,high))
    assert left[0] >= right[0] > 1 and left[1] <= right[1]
    assert all(a%2 == 0 and a <= c for a,c in (left,right))
    # At fixed residue modulo 2^(bulks+1), every parity choice and bulk
    # cost branch is fixed. Raw time is quadratic and seed gain constant.
    charge_mod4 = (8*launch.even + 4*(launch.k+word.count('J')) + 5*word.count('L') + 5)%4
    assert charge_mod4 == 0  # The return gain is even, so this parity stays closed.
    return 2**(1+word.count('L'))


def direct(seed, cut):
    count = clock = 0
    while seed < cut:
        nxt,dt = timed_return(seed)
        assert nxt is not None and nxt > seed
        count += 1
        clock += dt
        seed = nxt
    return seed,count,clock


def verify_scaled_phase(rows, worker):
    scaled = HALTING_TARGET//3**257
    assert scaled == 51_428_028_152_740_925 and all(i in rows for i in range(279))
    a,b = CUTS[279],scaled-100_000
    start = b+84
    receipt = (a,b,start,start,90_637,220_284_460)
    if worker:
        line = subprocess.check_output([worker.resolve(),str(a),str(b)],text=True)
        assert tuple(map(int,line.split())) == receipt
    previous = 51_428_028_152_740_789
    assert direct(start,previous)[:2] == (previous,629)
    nxt,_ = timed_return(previous)
    assert previous < scaled <= nxt and nxt == 51_428_028_152_740_994
    print(f'The two successive resets around floor(H/3^257) lie at offsets {previous-scaled} and +{nxt-scaled}.')


def verify(table, worker=None, clock=False):
    rows = read_table(table)
    assert all(i in rows for i in range(170))
    a,b,first,last,_,_ = APPROACH
    assert CUTS[170] == a and b <= first <= last <= b+5000
    if worker:
        line = subprocess.check_output([worker.resolve(),str(a),str(b)],text=True)
        assert tuple(map(int,line.split())) == APPROACH
    assert coalesce(range(first,last+1),1268) == (SOURCE,1268)
    odd = certify_word(ODD_START,ODD_LAST,'LLLLLLLLLLJJJLLLLJLLLLJL')
    even = certify_word(EVEN_START,EVEN_LAST,'LLJLLJLLL')
    assert (odd,even) == (2**20,256)
    sections = [direct(SOURCE,ODD_START)]
    assert sections[-1][0] == ODD_START
    sections.append(first_pass(ODD_START,ODD_START,ODD_LAST,odd,200))
    sections.append(direct(sections[-1][0],EVEN_START))
    assert sections[-1][0] == EVEN_START
    sections.append(first_pass(EVEN_START,EVEN_START,EVEN_LAST,even,200))
    sections.append(direct(sections[-1][0],DESTINATION))
    assert [(s,n) for s,n,_ in sections] == [
        (ODD_START,305), (50_885_984_713_694_735,40_557_300), (EVEN_START,4),
        (51_054_820_342_878_432,1_648_785_441_234), (DESTINATION,25),
    ]
    assert sum(n for s,n,dt in sections) == 1_648_825_998_868
    assert sum(dt for s,n,dt in sections) == DURATION
    print(f'{SOURCE:,} to {DESTINATION:,} in 1,648,825,998,868 first returns and {DURATION:,} raw steps.')
    verify_scaled_phase(rows,worker)
    if clock:
        # The chain's selected increments are below REACH. See CROSSING_CLOCK_758.md.
        bounds = timed_extension(GOAL,SOURCE,[(GOAL,b,2*10**12)],PREVIOUS_CLOCK)
        bounds = tuple(t+DURATION for t in bounds)
        assert bounds == DESTINATION_CLOCK
        print(f'Blank clock at {DESTINATION:,} in [{bounds[0]:,}, {bounds[1]:,}].')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table',type=Path,default=TABLE)
    parser.add_argument('--worker',type=Path,help='replay the supplementary approach window')
    parser.add_argument('--clock',action='store_true')
    if not __debug__:
        parser.error('enable assertions to check the proof')
    args = parser.parse_args()
    verify(args.table,args.worker,args.clock)
