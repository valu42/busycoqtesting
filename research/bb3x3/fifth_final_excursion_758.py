"""A targeted inverse restriction for any hit on the fifth #758 terminal."""
from check_bb33 import champion_step
from check_confluence import itinerary
from fifth_crossing_758 import E_WORD, K, post_exception
from terminal_forest_758 import predecessors

ROOTS = (K - 73, K - 71, K, K + 2)
LOW = K - 10**11
ODD_CORRIDOR = 30_018_927_059_399_751


def check_exception_band():
    lo, hi = 2*LOW + 1, 2*(K + 2) + 1
    # Every possible E input has mass 11 mod 12. Pre-R phases have left
    # coordinates nondecreasing in that mass, right coordinates nonincreasing.
    excess = {}
    for residue in (11, 23, 35, 47):
        first = lo + (residue - lo) % 48
        last = hi - (hi - residue) % 48
        assert first <= last
        left = first + 6, 1
        right = last + 6, 1
        for op in E_WORD:
            a, c = left
            b, d = right
            assert a <= b and c >= d and a % 2 == b % 2
            assert a > 1 or a % 2 == 0  # Exclude an intermediate first reset.
            for x, y in (left, right):
                if op == 'L':
                    assert x >= 4 * ((y + 1) // 4) + 3
                else:
                    assert x <= y and (x % 2 == 1) == (op == 'J')
            left = champion_step(*left)
            right = champion_step(*right)
        assert left[0] == right[0] == 1
        assert right[1] - left[1] == (last - first) // 2
        excess[residue] = left[1] - (first - 1) // 2
        assert post_exception(first) == left[1]
        assert post_exception(last) == right[1]
    assert excess == {11: 326, 23: 328, 35: 324, 47: 326}
    residues = {(w // 2 + gain) % 24 for w, gain in excess.items()}
    assert residues == {3, 5, 13, 19}
    assert residues.isdisjoint(s % 24 for s in ROOTS)
    return excess


def verify():
    check_exception_band()
    odd_word = 'J' * 33 + 'LR'
    for s in (ODD_CORRIDOR, K + 1):
        assert itinerary(s) == (odd_word, 150)
    assert itinerary(ODD_CORRIDOR - 2)[0] != odd_word

    # A reset can have an L-parent only at c = 5 mod 6. Such a parent
    # has even left coordinate and therefore itself needs a bulk parent.
    assert [s for s in ROOTS if s % 6 == 5] == [K - 73]
    q = (K - 73 - 5) // 6
    for c in (4*q - 1, 4*q + 1):
        state = 4*q + 4, c
        assert champion_step(*state) == (1, K - 73)
        assert not predecessors(*state)

    min_calls = (2*min(ROOTS) + 1 - (2*LOW + 1 + 8) + 8) // 9
    assert min_calls == 22_222_222_206
    # Before the first root comes R (gain 5 in W), and before R comes L
    # (gain 5 or 9), hence the six possible odd/odd mass coordinates u.
    offsets = sorted({s - gain - K for s in ROOTS for gain in (5, 7)})
    assert offsets == [-80, -78, -76, -7, -5, -3]
    print(f'The first local root requires at least {min_calls:,} E-free calls; '
          f'the penultimate call is L at u-K in {offsets}.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O to check assertions.')
    verify()
