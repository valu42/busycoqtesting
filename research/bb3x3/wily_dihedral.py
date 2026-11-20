"""Check the six-valued Wily excursion invariant and the endpoint transfer matrix."""
from collections import Counter
from itertools import product

from check_bb33 import WILY
from wily_integer_map import START, image
from wily_orbit_sieve import POSITIVE_ENTRANCE


def compose(f, g):
    """Compose affine permutations z -> slope*z + offset of Z/3Z."""
    return f[0] * g[0], (f[0] * g[1] + f[1]) % 3


IDENTITY = (1, 0)
X, Y = (1, 2), (-1, 1)
J, C = (-1, 0), (1, 1)
DIGITS = (X, Y)
CARRIES = (Y, X, C, J)
PERMUTATIONS = tuple(product((-1, 1), range(3)))


def raw_label(n):
    """Product of the digits of n/3, stopping at an aligned alternating tail."""
    if n % 3 == 0:
        raise ValueError('numerator must be prime to three')
    label = IDENTITY
    width = 0
    while n not in (-2, -1) or width % 4:
        bit = n % 2
        label = compose(label, DIGITS[bit])
        n = (n - 3 * bit) // 2
        width += 1
    return label


def invariant(n):
    label = raw_label(n)
    return compose(Y, label) if n % 2 else label


def forest_children(state):
    residue, label = state
    long_right = J if residue == 1 else (-1, 2)
    short_right = Y if residue == 1 else C
    long = compose(compose(J, label), long_right)
    short = compose(compose(C, label), short_right)
    return (residue, long), (3 - residue, short)


def check():
    for mode, row in enumerate(WILY.rules):
        for bit, (written, outgoing) in enumerate(row):
            next_carry = IDENTITY if outgoing == -1 else CARRIES[outgoing]
            assert compose(CARRIES[mode], DIGITS[bit]) == compose(DIGITS[written], next_carry)
    for pair in ((X, Y), (Y, X)):
        product_label = compose(*pair)
        assert compose(product_label, product_label) == IDENTITY

    def inverse_affine(f):
        return f[0], (-f[0] * f[1]) % 3

    for h, expected in ((0, (-1, 2)), (2, IDENTITY), (3, (-1, 2))):
        extension = IDENTITY
        for bit in WILY.extension[h]:
            extension = compose(extension, DIGITS[bit])
        assert compose(inverse_affine(CARRIES[h]), extension) == expected

    for n in range(-6000, 6001):
        if n % 3 == 0:
            continue
        successor = image(n)
        if n % 3 == successor % 3:
            assert invariant(n) == invariant(successor)
        else:
            right = Y if n % 3 == 1 else C  # The inverse of the carry still active at the cutoff.
            assert invariant(successor) == compose(invariant(n), right)
        long = 4 * n + 6
        short = 2 * n + (-3 if n % 2 else 9)
        assert forest_children((n % 3, raw_label(n))) == tuple(
            (m % 3, raw_label(m)) for m in (long, short))
    assert invariant(START) == invariant(POSITIVE_ENTRANCE) == IDENTITY
    assert [invariant(n) for n in (-8, -16, -26, -7, -58, -23, -62)] == [
        Y, X, (-1, 2), J, X, J, IDENTITY]

    states = tuple(product((1, 2), PERMUTATIONS))
    for branch in range(2):
        assert {forest_children(s)[branch] for s in states} == set(states)
    for start in states:
        paths = Counter({start: 1})
        for _ in range(6):
            next_paths = Counter()
            for s, count in paths.items():
                for child in forest_children(s):
                    next_paths[child] += count
            paths = next_paths
        assert len(paths) == 12 and min(paths.values()) >= 1

    # Last lift fixes parity: long is even, short is odd.
    paths = Counter((n % 3, raw_label(n)) for n in (-8, -16))
    passing = []
    for _ in range(10):
        next_paths = Counter()
        hits = 0
        for s, count in paths.items():
            long, short = forest_children(s)
            if long == (1, IDENTITY):
                hits += count
            if short == (1, Y):
                hits += count
            next_paths[long] += count
            next_paths[short] += count
        paths = next_paths
        passing.append(hits)
    assert passing == [0, 0, 1, 2, 6, 9, 21, 36, 82, 165]
    print('Blank invariant: identity. Escape roots: reflection 1-z, translation z-1.')
    print('Passing sign-escape endpoints in generations 1 through 10:', passing)
    print('Both branches permute 12 labels; all sixth-power matrix entries are positive.')


if __name__ == '__main__':
    check()
