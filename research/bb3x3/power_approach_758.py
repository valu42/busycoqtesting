"""Wide upstream power gates and the raw clock on the approach to 3^292."""
from check_bb33 import champion_step
from check_confluence import itinerary
from target_clock_758 import first_pass, timed_return

EXPONENT = 292
POWER = 3**EXPONENT
START = (1458*POWER-876_528)//1475-1
CHECKPOINT = POWER+1_934_340


def check_words(m, start):
    power = 3**m
    end = power-2*m-4
    cap = 0
    for parity,word in ((0,'J'*(m-1)+'LLJLLLR'),(1,'J'*(m-2)+'LR')):
        lo = start+(parity-start)%2
        hi = end-(end-parity)%2
        pattern,growth = itinerary(lo)
        assert pattern == word and itinerary(hi) == (word,growth)
        # Exclude an internal visit to a=1 on the largest seed of each parity.
        # Along the fixed prefix its left counter is minimal for this parity.
        a,c = champion_step(1,hi)
        for _ in word[:-1]:
            assert a > 1
            a,c = champion_step(a,c)
        assert a > 1 and champion_step(a,c)[0] == 1
        cap = max(cap,growth//2)
    return cap


def verify():
    for m in range(20,293):
        p = 3**m
        start = (1458*p)//1475-2*m
        cap = check_words(m,start)
        old_start = (9999*p+9999)//10000
        old_end = p-2*m-4-34*(4*m+40)
        assert start < old_start and old_start+cap <= old_end

    assert (1458*POWER-876_528)%1475 == 0
    cap = check_words(EXPONENT,START)
    assert itinerary(START-1)[0] != itinerary(START+1)[0]
    edge = POWER-2*EXPONENT-4
    # Both parity words have at most five Ls, so a shift by 64
    # preserves every fine branch in either word.
    seed,count,clock = first_pass(START,START,edge,64,cap)
    while seed < CHECKPOINT:
        seed,dt = timed_return(seed)
        count += 1
        clock += dt
    assert seed == CHECKPOINT
    assert clock//10**398 == 5226222591948275
    assert count//10**119 == 4025747469355849
    cut = edge-34*(4*EXPONENT+40)
    sufficient = 2*(cut-START+1)//9
    assert sufficient//10**121 == 5343807011174580
    print('all 273 widened power gates verified')
    print('scale 292 lower endpoint',START,'upper endpoint',cut)
    print('sufficient recent-reset distance in counter calls',sufficient)
    print('exact first returns',count,'raw transitions',clock)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O so verification checks execute.')
    verify()
