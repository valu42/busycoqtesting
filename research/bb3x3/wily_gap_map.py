"""One Wily scalar update on finite lists of zero gaps, with an implicit all-one tail."""
from itertools import product

from wily_integer_map import START, image
from wily_orbit_sieve import POSITIVE_ENTRANCE


def trim(gaps):
    gaps = list(gaps)
    while gaps and gaps[-1] == 1:
        gaps.pop()
    return tuple(gaps)


def encode(n):
    if n % 3 == 0:
        raise ValueError('numerator must be prime to three')
    gaps = []
    zeros = 0
    while n != -2 or zeros:
        bit = n % 2
        n = (n - 3 * bit) // 2
        if bit:
            gaps.append(zeros)
            zeros = 0
        else:
            zeros += 1
    return trim(gaps)


def decode(gaps):
    n = -2
    for a in reversed(gaps):
        n = (3 + 2 * n) << a
    return n


def gap_step(gaps):
    """Return the canonical output, number of recursive tokens, and stopping rule."""
    gaps = trim(gaps)
    padded = gaps + (1, 1, 1, 1)
    out = []
    i = 0
    increment = 0
    while i < len(gaps):
        first = padded[i]
        if first == 1:
            out.append(increment)
            i += 1
        elif first == 0 and padded[i + 2] == 0:
            out.append(increment + padded[i + 1] + 1)
            i += 3
        else:
            tokens = len(out)
            if first == 2:
                out.extend((increment, 0, padded[i + 1] + 1))
                i += 2
                kind = 'two'
            elif first >= 3:
                out.extend((increment, 0, 0, first - 3))
                i += 1
                kind = 'large'
            elif padded[i + 2] == 1:
                out.extend((increment + padded[i + 1] + 1, 0, padded[i + 3] + 1))
                i += 4
                kind = 'zero-one'
            else:
                out.extend((increment + padded[i + 1] + 1, 0, 0, padded[i + 2] - 2))
                i += 3
                kind = 'zero-large'
            out.extend(padded[i:])
            return trim(out), tokens, kind
        increment = 1
    tokens = len(out)
    out.append(increment)  # F on all-one gaps is 0 followed by all-one gaps.
    return trim(out), tokens, 'singular'


def height(gaps):
    return sum((1 if i % 2 == 0 else -1) * (a - 1) for i, a in enumerate(gaps))


def exits(gaps):
    """The complete negative-to-positive language. Trailing unit gaps are implicit."""
    gaps = trim(gaps)
    i = 0
    while i < len(gaps):
        if gaps[i] == 1:
            i += 1
        elif i + 2 < len(gaps) and gaps[i] == gaps[i + 2] == 0:
            i += 3
        else:
            break
    rest = gaps[i:]
    return rest in ((3,), (4,)) or (
        len(rest) == 3 and rest[0] == 0 and rest[2] in (2, 3))


def check_word(gaps):
    gaps = trim(gaps)
    n = decode(gaps)
    assert encode(n) == gaps
    assert (n > 0) == (len(gaps) >= 2 and gaps[-1] == 0)
    result, tokens, rule = gap_step(gaps)
    assert decode(result) == image(n)
    lift = 0 if rule == 'singular' else 3 * (-1) ** tokens
    assert height(result) == -height(gaps) - 1 + lift
    assert exits(gaps) == (n < 0 < image(n))


def main():
    for n in range(-8000, 8001):
        if n % 3:
            check_word(encode(n))
    for k in range(6):
        for w in product(range(6), repeat=k):
            check_word(w)
    assert encode(START) == (6, 2, 5, 1, 1, 6, 2, 3, 1, 1, 2, 2, 1, 3, 1, 1, 6, 2, 1, 0, 2)
    assert (height(encode(START)), height(encode(POSITIVE_ENTRANCE))) == (6, 0)
    print('Blank checkpoint gap word:', encode(START))
    print('Signed heights for the checkpoint and its positive entrance: 6 and 0.')
    print('Checked integer conjugacy, sign, exact exit language, and the height lift.')


if __name__ == '__main__':
    main()
