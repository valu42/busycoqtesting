"""Check integer height increments and the high phases of periodic Wily shadows."""
from itertools import product

from check_bb33 import WILY, sweep
from wily_gap_map import encode, height

DIGITS = ((1, -1), (-1, 1))
CARRIES = ((-1, 1), (1, -1), (1, 1), (-1, 0))
IDENTITY = (1, 0)


def compose(left, right):
    return left[0] * right[0], left[0] * right[1] + left[1]


def digit_product(word):
    label = IDENTITY
    for bit in word:
        label = compose(label, DIGITS[bit])
    return label


def at_one(isometry):
    return sum(isometry)


def word_height(word):
    return -at_one(digit_product(word))


def check_local():
    for mode, row in enumerate(WILY.rules):
        for bit, (written, outgoing) in enumerate(row):
            left = compose(CARRIES[mode], DIGITS[bit])
            right = compose(DIGITS[written], IDENTITY if outgoing == -1 else CARRIES[outgoing])
            assert left[0] == right[0]
            assert left[1] - right[1] == (-3 if (mode, bit) == (1, 0) else 0)
    for mode, difference in ((0, 0), (2, 3), (3, 0)):
        extension = digit_product(WILY.extension[mode])
        assert at_one(CARRIES[mode]) - at_one(extension) == difference


def check_recurrent_pairs():
    # Only 0, 1, 2 can survive indefinitely in both consecutive singular sweeps.
    states = list(product(range(3), repeat=2))
    closure = {state: {state} for state in states}
    edges = []
    for state in states:
        first, second = state
        for bit in (0, 1):
            middle, a = WILY.rules[first][bit]
            _, b = WILY.rules[second][middle]
            if (a, b) in closure:
                closure[state].add((a, b))
                edges.append((state, bit, middle, (a, b)))
    for via in states:
        for state in states:
            if via in closure[state]:
                closure[state].update(closure[via])

    recurrent = [(state, bit, written) for state, bit, written, dest in edges
                 if state in closure[dest]]
    assert set(recurrent) == {((2, 2), 0, 0), ((0, 1), 0, 1), ((1, 0), 1, 0)}
    for (first, _), _, written in recurrent:
        extension = WILY.extension[first]
        assert extension is None or written != extension[0]


def check_physical(word):
    n = 3 * sum(bit << i for i, bit in enumerate(word)) - (1 << len(word))
    assert word_height(word) == height(encode(n))
    mode = 0
    prefix = []
    slope = 1
    discrepancy = None
    for k, bit in enumerate(word, 1):
        if mode == 1 and bit == 0:
            assert discrepancy is None
            discrepancy = slope
        if mode == -1:
            written = bit
        else:
            written, mode = WILY.rules[mode][bit]
        prefix.append(written)
        slope *= DIGITS[written][0]
        truncated = word_height(word[:k]) + word_height(prefix) + 1
        assert abs(truncated) <= 5
        if mode == -1:
            assert truncated == -3 * discrepancy

    result = sweep(WILY, word, 0)
    if mode == 1:
        assert result is None
        return
    difference = word_height(result) + word_height(word) + 1
    if mode in (-1, 3):
        assert difference == -3 * discrepancy
    elif mode == 2:
        assert discrepancy is None and difference == 3 * slope
    else:
        assert mode == 0 and discrepancy is None and difference == 0


def main():
    check_local()
    check_recurrent_pairs()
    for width in range(13):
        for word in product((0, 1), repeat=width):
            check_physical(word)
    print('Verified the three recurrent carry-pair edges and the integer lift on 8,191 words.')


if __name__ == '__main__':
    main()
