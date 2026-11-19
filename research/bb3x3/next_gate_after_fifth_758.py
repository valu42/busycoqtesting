"""A sufficient next gate above the fifth candidate of BB(3,3) #758."""
from check_confluence import itinerary
from fifth_crossing_758 import K
from power_gates_758 import coarse_return, coalesce, gate_exits

START = K + 118
CUT = 49_454_910_341_926_411
GOAL = 3**35 + 34_754


def verify():
    m = 35
    power = 3**m
    last_odd = power-2*m-4
    first_even = CUT+1
    for parity, start, last, limit in (
        (0, first_even, last_odd + 2*m+7, 2*m+29),
        (1, START+1, last_odd, 2*m+5),
    ):
        for seed in (start, last-(last-parity)%2):
            assert seed % 2 == parity
            gain = coarse_return(m, seed, 1)-seed
            assert 0 < gain <= limit and gain % 2

    # The preceding even seed changes word; the odd seed CUT is included.
    try:
        coarse_return(m, first_even-2, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError('the lower endpoint is not sharp for even seeds')
    low = (9999*power+9999)//10000
    margin = 34*(4*m+40)
    assert CUT+5_000 < low and low+2*m+29 < last_odd-margin
    exits = gate_exits(m, 1)
    assert len(exits) == 13 and coalesce(exits, 550) == (GOAL, 550)

    # The existing exponent-34 paired worker is sound on the entire gap.
    p = 3**34
    assert 2*p <= START < CUT <= 3*p-2*34-6-50_000
    cuts = [*range(START, CUT, 10**13), CUT]
    assert len(cuts)-1 == 897

    # Odd inputs normalize to even after one exact return of gain <=75.
    # Matching ordinary endpoint words certify a selected live reset for
    # every even input up to the next cut. The mass-charge limit remains
    # valid if the selected return has an earlier intermediate reset.
    simple = 0
    for a,b in zip(cuts,cuts[1:]):
        assert a+5_000+75 < b and b+5_000 < last_odd
        left = itinerary(a+a%2)
        right = itinerary(b-1-(b-1)%2)
        common_word, mass_gain = left
        if (left == right and common_word.endswith('R') and 'E' not in common_word
                and mass_gain//2+75 <= 5_000):
            simple += 1
    assert simple == 763


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions to check the guards.')
    verify()
    print('Single ordinary words certify 763 of 897 next windows.')
    print(f'Entry in {CUT:,}..{CUT+5_000:,} forces a visit to reset {GOAL:,}.')
