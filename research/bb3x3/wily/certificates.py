"""Exact, dependency-free checks for the Wily Coyote automata partial results.

These finite checks validate implementations and expose errors. Universal claims
in LANGUAGE_OBSTRUCTIONS.md are proved mathematically, not inferred from checks.
"""
from __future__ import annotations
from itertools import product
import re

# Five streaming states: s0, s1, s2, s3, and identity/copy.
STEP = (((1, 1), (0, 2)), ((1, 3), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (0, 4)), ((0, 4), (1, 4)))
END = ('0', None, '1100', '00', '')
BAD_RE = re.compile(r'(?:01|10*11)*(?:0|10*1)\Z')

def pass_word(word: str, mode: int = 0) -> str | None:
    out = []
    for ch in word:
        bit, mode = STEP[mode][int(ch)]
        out.append(str(bit))
    end = END[mode]
    return None if end is None else ''.join(out) + end

def sweep(word: str) -> str | None:
    out = pass_word(word)
    return None if out is None else '0' + out

def bad_dfa(word: str) -> bool:
    """Minimal four-state DFA: states 0,1,2 and safe sink 3."""
    trans = ((1, 2), (3, 0), (2, 1), (3, 3))
    q = 0
    for b in word:
        q = trans[q][int(b)]
    return q == 1

def words(n: int):
    return (''.join(bits) for bits in product('01', repeat=n))

def run_modes(word: str, modes: list[int]) -> str:
    """Require every selected pass to be safe and length preserving."""
    n = len(word)
    for mode in modes:
        out = pass_word(word, mode)
        assert out is not None and len(out) == n, (word, mode, out)
        word = out
    return word

def flip_bit(word: str, j: int) -> tuple[str, list[int]]:
    """Construct safe passes from modes 1,2,3 that flip only bit j.

    This is an induction on j. No enumeration or bounded-state search is used
    by the construction. The runtime can be exponential, which is harmless
    for its role as an existence certificate.
    """
    assert 0 <= j < len(word)
    original = word
    modes: list[int] = []

    def act(mode: int):
        nonlocal word
        word = run_modes(word, [mode])
        modes.append(mode)

    def set_lower(prefix: str):
        nonlocal word
        for i, desired in enumerate(prefix):
            if word[i] != desired:
                word, lower_modes = flip_bit(word, i)
                modes.extend(lower_modes)

    if j == 0:
        act(3)
    elif j == 1:
        set_lower('0')
        act(1)  # P1(0 b u) = 1 (!b) u.
        set_lower(original[:j])
    else:
        set_lower('0' * (j - 2) + '10')
        act(2)  # P2(0^(j-2) 1 0 b u) = 0^(j-2) 1 1 (!b) u.
        set_lower(original[:j])
    expected = original[:j] + str(1 - int(original[j])) + original[j + 1:]
    assert word == expected
    return word, modes

def transport(source: str, target: str) -> list[int]:
    assert len(source) == len(target)
    modes: list[int] = []
    for j in range(len(source)):
        if source[j] != target[j]:
            source, new = flip_bit(source, j)
            modes.extend(new)
    assert source == target
    return modes

def incoming_word(mode: int, length: int) -> str:
    """A word of prescribed sufficiently large length ending in any mode.

    The mode is the streaming state after the word, with no boundary action.
    Loops 01 and 111 at state s0 permit every padding length >= 2.
    Mode 4 is the identity state after early exit.
    """
    bases = ('', '0', '1', '00', '000')
    base = bases[mode]
    padding = length - len(base)
    assert padding >= 2
    if padding % 2:
        loop = '111' + '01' * ((padding - 3) // 2)
    else:
        loop = '01' * (padding // 2)
    word = loop + base
    q = 0
    for b in word:
        _, q = STEP[q][int(b)]
    assert len(word) == length and q == mode
    return word

def checks(max_word_length: int = 12, flip_length: int = 7) -> dict[str, int]:
    checked = 0
    for n in range(max_word_length + 1):
        for word in words(n):
            is_bad = pass_word(word) is None
            assert is_bad == bool(BAD_RE.fullmatch(word)) == bad_dfa(word)
            for k in (0, 1, 4):
                lhs = sweep('01' * k + word)
                rhs = sweep(word)
                assert lhs == (None if rhs is None else '01' * k + rhs)
            if word:
                first = sweep('00' + word)
                assert first is not None
                second = sweep(first)
                out = pass_word(word)
                assert second == (None if out is None else '0100' + out)
            checked += 1
    assert sweep(sweep('00')) == '0100' + '001100'
    controls = 0
    for n in range(1, flip_length + 1):
        for source in words(n):
            for j in range(n):
                target, modes = flip_bit(source, j)
                assert run_modes(source, modes) == target
                controls += 1
            target = '0' * (n - 1) + '1'
            assert run_modes(source, transport(source, target)) == target
            assert pass_word(target, 2) is None
    for mode in range(5):
        for n in range(6, 25):
            incoming_word(mode, n)
    # A count-only invariant already fails at the first generated word.
    assert sweep('00') == '01100'
    assert sorted('01100') == sorted('10001')
    assert pass_word('10001') is None
    return {'words_checked': checked, 'bit_flip_certificates_checked': controls}

if __name__ == '__main__':
    print(checks())
