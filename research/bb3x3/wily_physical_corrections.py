#!/usr/bin/env python3
"""Finite certificates for Wily's physical corrections and mixed-sign nonblank runs."""
from itertools import product

from check_bb33 import WILY, sweep
from wily_edge_stream import period_through
from wily_integer_map import advance, canonical_bucket, encode, image


def digits(word):
    return tuple(map(int, word))


def through_bits(period, bits):
    for bit in bits:
        period = period_through(period, bit)
    return period


def edge(period):
    extension = WILY.extension[period[0]]
    if extension is None:
        return None
    return through_bits(period[1:] + period[:1], extension)


def correction_preimage(output):
    """Reconstruct the unique nonempty input word from its corrected output."""
    if output[-3:] != (1, 0, 0):
        return None
    zeros = 0
    result = []
    i = 0
    while i < len(output) - 1:
        if output[i] == 0:
            zeros += 1
            i += 1
            continue
        if output[i:i + 2] != (1, 0):
            return None
        if zeros == 0:
            result.extend((0, 1))
        else:
            result.extend((1,) + (0,) * (zeros - 1) + (1, 1))
        zeros = 0
        i += 2
    if zeros or i != len(output) - 1:
        return None
    return tuple(result)


def check_language():
    for width in range(1, 13):
        produced = set()
        for word in product((0, 1), repeat=width):
            p, capacity = encode(word)
            following, next_capacity, mode = advance(p, capacity)
            if mode != 0:
                continue
            actual = sweep(WILY, word, 0)
            assert actual not in produced
            produced.add(actual)
            assert correction_preimage(actual) == word
            assert capacity == canonical_bucket(p)
            assert next_capacity == canonical_bucket(following) == 2 * capacity
            assert following == image(p + 6 * capacity)
            assert (p - image(p)) % 3 == 0
            assert (p + 6 * capacity - following) % 3 != 0
        expected = {word for word in product((0, 1), repeat=width + 1)
                    if word[-3:] == (1, 0, 0) and (1, 1) not in zip(word, word[1:])}
        assert produced == expected


def check_mixed_cycle():
    x = digits("01011000110110110101")
    y = digits("101000001010001010100")
    assert correction_preimage(y) == x and sweep(WILY, x, 0) == y
    assert advance(*encode(x)) == (*encode(y), 0)
    before = digits("23211301122322222")
    a = digits("222303111030")
    b = digits("303222030")
    c = digits("311103022230")
    d = digits("211111122303030")
    assert through_bits((0,), y) == before
    assert all(edge(left) == right for left, right in
               ((before, a), (a, b), (b, c), (c, d), (d, a)))
    # At c the first two events enlarge by 00 and then write 11 and stop.
    assert c[:2] == (3, 1) and WILY.extension[3] == (0, 0)
    assert WILY.rules[1][0] == (1, 3) and WILY.rules[3][0] == (1, -1)
    assert sum(len(WILY.extension[p[0]]) for p in (a, b, c, d)) == 12

    pair = (1, 0)
    suffix = digits("000000100")
    assert through_bits(before, pair * 2) == a
    assert through_bits(a, pair * 6) == a
    entry = digits("222030303030303222")
    assert through_bits(a, suffix) == entry and edge(entry) == c
    for j in (0, 1, 2):
        output = y + pair * (2 + 6 * j) + suffix
        word = correction_preimage(output)
        assert word is not None
        assert sweep(WILY, word, 0) == output
        assert advance(*encode(word)) == (*encode(output), 0)


def check_blank_seed():
    physical = digits("10100101010100010010101000100")
    seed = digits("222030111101130321301012")
    previous = correction_preimage(physical)
    assert encode(physical) == (-318_922_769, 1 << 29)
    assert previous is not None and advance(*encode(previous)) == (*encode(physical), 0)
    p, capacity = encode(previous)
    assert p + 6 * capacity == 2_031_034_478
    assert through_bits((0,), physical) == seed

    for initial, expected in ((0, 2), (1, 1), (2, 3), (3, -1)):
        bits = [1, 0]
        live = initial
        for i, bit in enumerate(bits):
            bits[i], live = WILY.rules[live][bit]
            if live == -1:
                break
        assert live == expected
        if initial == 3:
            assert bits == [0, 0]
        if initial == 2:
            assert bits == [1, 1]

    virtual, actual, levels = seed, seed, 0
    while levels < 18:
        assert virtual == actual
        mode = actual[0]
        assert mode in (2, 3)
        actual = edge(actual)
        virtual = through_bits(virtual, (1, 0))
        levels += 1
        if mode == 2:
            assert virtual[0] == 3
            virtual = through_bits(virtual, (1, 0))
            levels += 1


BLOCKS = {0: (3, 1), 1: (0, 3), 2: (2,), 3: (1, 3)}
MARK = (3, 1, 2, 0)


def one_cell(block):
    bit = 0
    output = []
    for event in block:
        bit, carry = WILY.rules[event][bit]
        if carry != -1:
            output.append(carry)
    return bit, tuple(output)


def check_reset_lift():
    for event, block in BLOCKS.items():
        assert one_cell(block) == (0, (event,))
    assert one_cell((3,) + MARK) == (0, MARK[:3])
    assert one_cell((3,) + MARK + (3, 1)) == (0, MARK)
    safe = tuple(map(digits, ("0312003312", "0212312", "231312", "30", "30")))
    halt = tuple(map(digits, ("0033120312", "1021312"))) + (None,)
    for chain in (safe, halt):
        assert all(edge(x) == y for x, y in zip(chain, chain[1:]))

    # M denotes 3120. Each cut starts at the 0 of the distinguished M.
    def rotated(tokens, cut):
        i = tokens.index(cut)
        others = tokens[i + 1:] + tokens[:i]
        middle = tuple(c for token in others for c in (MARK if token in "AB" else digits(token)))
        return (0,) + middle + MARK[:3]

    tokens = "AB03"
    assert (rotated(tokens, "A"), rotated(tokens, "B")) == (safe[0], halt[0])
    for _ in range(5):
        following = "".join("3" + token + "31" if token in "AB" else
                            "".join(map(str, BLOCKS[int(token)])) for token in tokens)
        for mark in "AB":
            assert edge(rotated(following, mark)) == rotated(tokens, mark)
        tokens = following


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("run with assertions enabled")
    check_blank_seed()
    check_language()
    check_mixed_cycle()
    check_reset_lift()
    print("Correction language, physical mixed-sign cycle, pumped starting tapes and rotation lift verified.")
