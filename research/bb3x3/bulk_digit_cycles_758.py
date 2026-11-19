"""Verify charge flags, physical words, possible entrances and blank-cycle bounds."""
from fractions import Fraction as F
from math import ceil, comb, floor
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit("Run with assertions enabled.")

# Permit use from the staged research workspace and after copying to research/bb3x3.
if not (Path(__file__).parent / 'check_bb33.py').exists():
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'research/bb3x3'))
from check_bb33 import HALTING_TARGET, first_return
from double35_frontier_758 import CUTS, TABLE, read_table
from scale_clauses_758 import check_word
from fifth_blank_clock_758 import timed_extension
from power35_inner_skip_758 import GOAL, PREVIOUS_CLOCK
from target_clock_758 import timed_return


def flags(y, length):
    word = 0
    for i in range(length):
        word |= (y & 1) << i
        y = 3*((y+1)//2)
    return y, word


def corridor(m, b):
    assert b % 2 == 1
    power = 3**m
    ratio = F(4,9)**((b-1)//2)
    lower = 1 - ratio*F(2,3) + F(20,power)
    upper = 1 - ratio*F(4,9) - F(20,power)
    assert upper > lower > 0
    lo = floor(power/upper - 2*m) + 1
    hi = ceil(power/lower - 2*m) - 1
    odd_word = 'J'*m + 'L'*b + 'R'
    for seed in (lo+(1-lo)%2, hi-(hi-1)%2):
        gain = check_word(seed, odd_word)
        y = (seed-power+2*m+8)//2
        assert gain == 2*m + 5*(b+1)//2 + 2*flags(y,b)[1].bit_count()
        assert seed+gain == first_return(seed)
    return lo, hi


def verify_small():
    for b in range(1,11):
        p = 2**b
        words = [flags(y,b)[1] for y in range(p)]
        assert len(set(words)) == p
        for depth in range(b):
            for r in range(2**depth):
                weights = [w.bit_count() for w in words[r::2**depth]]
                base = flags(r,depth)[1].bit_count()
                for k in range(b-depth+1):
                    assert weights.count(base+k) == comb(b-depth,k)
        w = [word.bit_count() for word in words]
        assert all(abs(w[i]-w[i+p//2]) == 1 for i in range(p//2))
    f = [flags(y,3)[1] for y in range(4)]
    assert f == [0,3,2,5] and f[1]^f[2]^f[0] != f[3]
    b, m = 7,35
    c = m+5*(b+1)//4
    q = [(2*n+c+flags(2*n,b)[1].bit_count()+1)//2 for n in range(2**(b-1))]
    assert (q[15],q[16]) == (40,39)
    assert len({s % 64 for s in q}) == 45


def verify_physical():
    lo, hi = corridor(35,27)
    assert (lo,hi) == (50_032_132_174_230_649, 50_032_425_717_012_734)
    assert CUTS[0] <= lo <= hi <= CUTS[1] and 0 in read_table(TABLE)
    even_word = 'I' + 'J'*34 + 'LLJLLLR'
    for seed in (lo+1,hi):
        assert seed%2 == 0
        assert check_word(seed,even_word) in range(89,100,2)
    period = 1_606_408
    transients = 1_631_454-period+1
    odd_arrival = lo+100_101
    seed_after_transient = odd_arrival+194*transients
    repetitions = (hi-seed_after_transient)//2**28
    assert (transients, repetitions, repetitions*period) == (25_047,1_093,1_755_803_944)
    lo292, hi292 = corridor(292,255)
    assert hi292-lo292 > 2**256+10 and hi292 < HALTING_TARGET
    middle = (lo292+hi292)//2
    even292 = 'I'+'J'*291+'LLJLLLR'
    for seed in (lo292+lo292%2,hi292-hi292%2):
        assert check_word(seed,even292) in range(603,616,2)
    assert (2*(middle-lo292)-20)//9 > 96*10**91
    assert (2**255+866)//867 > 66*10**72
    cycle_span = 1734 * 2**254
    assert (hi292-middle-615-1734)//cycle_span-1 >= 8*10**13
    b,l = 255,98
    assert 2**(b-l) > 3**l+3*F(3,2)**l
    assert not 2**(b-l-1) > 3**(l+1)+3*F(3,2)**(l+1)
    source = 50_032_132_179_190_025
    assert source+(repetitions << 28) == 50_032_425_579_143_433 <= hi
    assert timed_return(source) == (50_032_132_179_190_191, 9_762_379_791_435_097_453_128_986_287_146_657)
    initial = timed_extension(GOAL,source,[(GOAL,source,2*10**12)],PREVIOUS_CLOCK)
    duration = 15_968_388_026_771_997_073_986_594_690_949_338_871_473_882
    final = tuple(bound+duration for bound in initial)
    assert final == (1_482_820_049_967_536_695_531_357_357_768_072_109_082_724_793_753,
                     1_988_656_487_065_207_573_055_806_856_562_561_840_865_874_936_083)
    print(f'#758 raw clock at the flight destination lies in [{final[0]:,}, {final[1]:,}].')
    print(f'Blank power 35 has at least {repetitions:,} full periods of {period:,} consecutive returns.')
    print(f'The physical power-292, 255-bulk word has at least {2**(l-2):,} distinct high-continuation functions.')


if __name__ == '__main__':
    verify_small()
    verify_physical()
