"""Exact raw clock from the fourth pair crossing to its synchronized checkpoint."""
from math import comb

from after_fourth_758 import CHECKPOINT, EVEN_END, K, ODD_END, increments
from check_bb33 import champion_step
from exact_fourth_758 import LOW, MERGER
from mass_clock_758 import raw_lower_bound
from timing_758 import branch_cost


def timed_return(seed):
    a,c = 1,seed
    elapsed = 0
    while True:
        elapsed += branch_cost(a,c)
        state = champion_step(a,c)
        assert state is not None
        a,c = state
        if a == 1:
            assert c > seed
            return c,elapsed


def cycle_cost(seed, length, stride):
    origin = seed
    clock = 0
    for _ in range(length):
        seed,dt = timed_return(seed)
        clock += dt
    assert seed == origin+stride
    return clock


def band(seed, end, modulus, gains):
    count = clock = 0
    seen = {}
    while seed <= end:
        residue = seed % modulus
        if residue in seen:
            old, index = seen[residue]
            stride = seed-old
            length = count-index
            assert stride > 0 and stride % modulus == 0
            copies = (end-seed)//stride
            if copies >= 4:
                costs = [cycle_cost(seed+j*stride,length,stride) for j in range(4)]
                a,b,c,d = costs
                second = c-2*b+a
                assert d-2*c+b == second
                clock += copies*a + comb(copies,2)*(b-a) + comb(copies,3)*second
                seed += copies*stride
                count += copies*length
            seen.clear()
        seen[seed % modulus] = seed,count
        nxt,dt = timed_return(seed)
        assert nxt-seed == gains[seed % modulus]
        seed = nxt
        clock += dt
        count += 1
    return seed,count,clock


def verify():
    start = K+65
    odd = increments(start,ODD_END,'J'*33+'L'*7+'R')
    seed,count,clock = band(start,ODD_END,*odd)
    while seed % 2:
        seed,dt = timed_return(seed)
        clock += dt
        count += 1
    even = increments(seed,EVEN_END,'J'*33+'LLJLR')
    seed,n,dt = band(seed,EVEN_END,*even)
    count += n
    clock += dt
    while seed < CHECKPOINT:
        seed,dt = timed_return(seed)
        clock += dt
        count += 1
    assert seed == CHECKPOINT and count == 10_747_030_481_905
    assert clock == 12_009_315_348_729_165_034_617_066_232_977_846_431_994_862_719
    seed = MERGER
    pre_clock = 0
    for _ in range(425):
        seed,dt = timed_return(seed)
        pre_clock += dt
    assert seed == LOW+208
    odd_prefix = increments(seed,ODD_END,'J'*33+'L'*7+'R')
    seed,n,dt = band(seed,K+1,*odd_prefix)
    assert seed == start and n == 791_921_888_157
    pre_clock += dt
    assert pre_clock == 868_964_390_669_458_400_613_660_337_140_973_728_114_577_608
    lower = raw_lower_bound(1+2*MERGER)+pre_clock+clock
    assert lower == 14_834_450_150_617_068_606_370_263_277_192_707_547_238_915_715
    print(f'{count:,} first returns, {clock:,} raw transitions. '
          f'Blank clock at the endpoint at least {lower:,} for #758.')
    return clock,lower


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O so verification checks execute.')
    verify()
