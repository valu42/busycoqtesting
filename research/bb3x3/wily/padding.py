#!/usr/bin/env python3
"""Exact periodic-tail / record-width reduction for Wily's a=s0 pass.

This module DOES NOT decide the blank orbit. The unbounded results are the
parameterized padding identities and running-maximum theorem documented in
TAIL_RENORMALIZATION.md. Finite checks below validate their implementation.
"""
from itertools import product

NEXT = ((1, 2), (3, 0), (2, 1), (4, 4), (4, 4))
OUTPUT = ((1, 0), (1, 0), (0, 1), (1, 0), (0, 1))
FINITE = ("0", None, "1100", "00", "")
VIRTUAL = ("001100", "0", "1100", "00", "")


def scan(word, mode=0):
    """Return emitted bits and residual mode BEFORE the boundary rule."""
    output = []
    for char in word:
        bit = int(char)
        output.append(str(OUTPUT[mode][bit]))
        mode = NEXT[mode][bit]
    return "".join(output), mode


def pass_word(word, mode=0):
    output, mode = scan(word, mode)
    suffix = FINITE[mode]
    return None if suffix is None else output + suffix


def canonical(word):
    """Unique (v,k) with word=v(10)^k and v not ending in 10."""
    k = 0
    while word.endswith("10"):
        word = word[:-2]
        k += 1
    return word, k


def numerator(word):
    """Three times the 2-adic value of word(10)^omega."""
    return 3 * sum(int(b) << i for i, b in enumerate(word)) - (1 << len(word))


def from_numerator(value):
    """Canonical finite representative of value/3, for value not in 3Z."""
    if value % 3 == 0:
        raise ValueError("The eventually alternating class excludes multiples of 3")
    width = 0 if value % 3 == 2 else 1
    while not (0 <= (value + (1 << width)) // 3 < (1 << width)):
        width += 2
    digits, remainder = divmod(value + (1 << width), 3)
    assert remainder == 0
    word = "".join(str((digits >> i) & 1) for i in range(width))
    assert not word.endswith("10")
    return word


def virtual_step(word):
    """Canonical output under the TOTAL infinite-tail automorphism a.

    Returns (canonical_output, residual_mode). Mode b is permitted here;
    it is exactly the singular event at which the finite pass would halt.
    """
    assert not word.endswith("10")
    emitted, mode = scan(word)
    return canonical(emitted + VIRTUAL[mode])[0], mode


def padded_formula(prefix, k):
    """Closed form for a(prefix+(10)^k), valid for every prefix and k>=0."""
    assert k >= 0
    emitted, mode = scan(prefix)
    if mode == 0:
        return emitted + ("0" if k == 0 else "001100" + "10" * max(k - 3, 0))
    if mode == 1:
        return None
    if mode == 2:
        return emitted + "1100" + "10" * max(k - 2, 0)
    if mode == 3:
        return emitted + "00" + "10" * max(k - 1, 0)
    return emitted + "10" * k


def record_step(word, record_width):
    """One exact finite a-step in canonical-word / record-width coordinates.

    Returns None at a halt, else (new_canonical_word,new_record_width,repair).
    The word represented is word+(10)^((record_width-len(word))/2).
    """
    assert not word.endswith("10")
    assert record_width >= len(word) and (record_width - len(word)) % 2 == 0
    emitted, mode = scan(word)
    if mode == 1:
        return None
    if mode == 0 and len(word) == record_width:
        following = emitted + "0"
        assert not following.endswith("10")
        virtual = emitted + "001100"
        assert numerator(following) == numerator(virtual) + 26 * (1 << len(word))
        return following, record_width + 1, True
    following = canonical(emitted + VIRTUAL[mode])[0]
    return following, max(record_width, len(following)), False


def reconstruct(word, record_width):
    assert record_width >= len(word) and (record_width - len(word)) % 2 == 0
    return word + "10" * ((record_width - len(word)) // 2)


def repair_language(word):
    """All possible outputs of a finite boundary-a repair."""
    return word == "0" or (word.endswith("100") and "11" not in word)


def verify():
    words = 0
    for length in range(11):
        for chars in product("01", repeat=length):
            word = "".join(chars)
            words += 1
            can, padding = canonical(word)
            assert reconstruct(can, len(word)) == word
            assert numerator(can) == numerator(word)
            assert from_numerator(numerator(word)) == can
            for k in range(9):
                assert pass_word(word + "10" * k) == padded_formula(word, k)
            result = record_step(can, len(word))
            direct = pass_word(word)
            if result is None:
                assert direct is None
            else:
                new, width, repair = result
                assert reconstruct(new, width) == direct
                if repair:
                    assert repair_language(new)
            virtual, mode = virtual_step(can)
            assert (numerator(virtual) % 3 != numerator(can) % 3) == (mode == 1)
            if mode == 4:
                assert len(virtual) - len(can) in (0, -2)
            elif mode == 1:
                assert len(virtual) == len(can) - 1
    for value in range(-2000, 2001):
        if value % 3:
            assert numerator(from_numerator(value)) == value
    # A finite illustration of the first actual repair, not an infinite proof.
    word = "001100"
    can, width = word, len(word)
    repairs = []
    for step in range(583):
        result = record_step(can, width)
        assert result is not None
        new, new_width, repair = result
        if repair:
            repairs.append((step, can, new))
        word = pass_word(word)
        assert word == reconstruct(new, new_width)
        can, width = new, new_width
    assert repairs == [
        (582, "0101111010101101111101011011", "10100101010100010010101000100")
    ]
    print("All parameterized-identity implementation checks passed:", words, "short words")
    print("First blank-core repair:", repairs[0])
    print("The all-depth competition between record-a repairs and b halts is unproved.")


if __name__ == "__main__":
    verify()
