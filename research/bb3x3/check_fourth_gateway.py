"""Verify the odd-reset corridor bypassing the fourth candidate terminal."""
import argparse
from check_bb33 import champion_step, first_return
from check_confluence import itinerary

K = 17_430_344_744_167_562
LOW = 17_354_320_242_904_343
EVEN_HIGH = 17_363_959_236_929_600
EXPECTED = ((-81, 19), (-65, 29), (-47, 47), (-35, 65), (-19, 79), (1, 95))


def verify_gateway():
    # itinerary() starts after the parity-specific initial move.
    odd_word = 'J'*33 + 'L'*7 + 'R'
    even_word = 'J'*33 + 'LLJLLJJLR'
    assert itinerary(LOW) == itinerary(K+1) == (odd_word, 204)
    assert itinerary(LOW-2)[0] != odd_word
    assert itinerary(LOW+1) == itinerary(EVEN_HIGH) == (even_word, 202)
    assert itinerary(EVEN_HIGH+2)[0] != even_word
    # The larger endpoint minimizes the left counter throughout the common
    # word. Each interior minimum is above one, so these are first returns.
    for seed, calls in ((K+1,42),(EVEN_HIGH,43)):
        a,c=1,seed
        for _ in range(calls-1):
            a,c=champion_step(a,c)
            assert a>1
        assert champion_step(a,c)[0]==1
    skipped_seeds = EVEN_HIGH-LOW+1
    assert (2*(skipped_seeds+1)+8)//9 == 2_141_998_672_280
    second_low = 17_393_401_372_077_661
    second_high = 17_408_159_912_737_553
    second_word = 'J'*33+'LLJLLJJJLR'
    assert itinerary(second_low+1) == itinerary(second_high-1) == (second_word,206)
    assert second_high+103+128*102 < K
    assert (2*(second_high-second_low+2)+8)//9 == 3_279_675_702_199
    assert EVEN_HIGH+101 < K
    # Fine-residue gains have period 256 on this ordinary odd word. Adding
    # 256 preserves c modulo four at each of seven Ls (one bit lost per L).
    gains = {}
    for residue in range(1, 256, 2):
        seed = LOW + (residue-LOW)%256
        delta = first_return(seed, batch=False)-seed
        assert delta%2 == 0 and 88 <= delta <= 102
        gains[residue] = delta
    cycle = set(gains)
    for _ in range(128):
        cycle = {(s+gains[s])%256 for s in cycle}
    assert {(s+gains[s])%256 for s in cycle} == cycle
    assert EVEN_HIGH+101+128*102 < K
    cycles = []
    exits = []
    while cycle:
        here = min(cycle)
        length = total = 0
        while here in cycle:
            cycle.remove(here)
            end_seed = K+2-(K+2-here)%256
            if end_seed+gains[here] > K+2:
                exits.append((end_seed-K, end_seed+gains[here]-K))
            length += 1
            total += gains[here]
            here = (here+gains[here])%256
        assert total%256 == 0
        cycles.append((length, total//256))
    assert sorted(cycles) == [(8,3), (8,3)]
    assert tuple(sorted(exits)) == EXPECTED
    print(f"{EVEN_HIGH-LOW+1:,} consecutive reset seeds bypass K; six possible crossings.")


def verify_local():
    for target in (K,K+2):
        assert first_return(target, batch=False) is None
    largest = 0
    for seed in range(K-1_000_000,K+3):
        if seed in (K,K+2):
            continue
        nxt = first_return(seed, batch=False)
        assert nxt is not None and nxt>seed and nxt not in (K,K+2)
        largest = max(largest, nxt-seed)
    assert largest == 388
    print("Only K and K+2 halt among the 1,000,003 seeds before passing the pair.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local',action='store_true',help='also replay the million-seed census')
    args=parser.parse_args()
    verify_gateway()
    if args.local:
        verify_local()
