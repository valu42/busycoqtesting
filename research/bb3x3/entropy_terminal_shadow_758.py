"""Verify uniformly congruent continuing lifts of the #758 halting template."""

from fractions import Fraction as F

from check_758_lifts import BASE_M, D, FINE, OFFSET, tail_states


def states(power, relative_shift):
    z = (3**15 * power - OFFSET) / D + relative_shift * power
    return tail_states(power, z)


def verify():
    # Exact positivity at P0 and nonnegative P slope give the inequalities
    # for every real P >= P0, hence for every admissible integer power.
    initial = F(3**BASE_M)
    for relative_shift in (F(-1, 10000), F(1, 10000)):
        base = states(initial, relative_shift)
        plus = states(initial + 1, relative_shift)
        for (a, c), (aa, cc), label in zip(base, plus, FINE + 'D'):
            assert min(a, c) > 7 and aa > a and cc > c
            if label == 'J':
                assert c - a > 7 and cc - aa >= c - a
            elif label in 'BC':
                assert a - c > 7 and aa - cc >= a - c
        # The gap before the final test is treated arithmetically below.
    # A unit seed shift after the common J run leaves the left coordinate
    # unchanged, and gives these derivatives throughout the affine suffix.
    paths = tuple(tail_states(F(1), F(z)) for z in (1, 2))
    shifts = [(aa - a, cc - c) for (a, c), (aa, cc) in zip(*paths)]
    assert all((2**15 * da).denominator == (2**15 * dc).denominator == 1
               and (2**15 * da) % 4 == (2**15 * dc) % 4 == 0
               for da, dc in shifts)
    assert shifts[-1] == (F(-4650361, 4096), F(4658553, 8192))
    da, dc = shifts[-1]
    assert da - dc == -F(D, 8192)
    print("Verified both 1/10000 margins, all 15 modular states, and the terminal gap slope.")


if __name__ == '__main__':
    verify()
