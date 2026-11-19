"""Check the integer halting guard and the matched-register witness for #397."""
from fractions import Fraction
from itertools import product

from check_bb33 import H397, sweep
from first_contact_397 import register
from regular_guard_397 import RETURN, one_return


TAIL = (1, 1, 1, 0)
EDGE = (-52, -22, -14, 53, 1, -97)
CORRECTED = (1, 2, None, 4, None, 23)


def integer(bits):
    return sum(b << i for i, b in enumerate(bits))


def segment(bits, mode):
    output = []
    for bit in bits:
        if mode != -1:
            bit, mode = H397.rules[mode][bit]
        output.append(bit)
    return tuple(output), mode


def periodic_image(bits, mode):
    """Exact 2-adic value of the infinitely repeated input after a carry."""
    base = 1 << len(bits)
    blocks = []
    seen = {}
    while mode not in seen:
        seen[mode] = len(blocks)
        output, mode = segment(bits, mode)
        blocks.append(integer(output))
    cut = seen[mode]
    prefix = sum(blocks[j] * base**j for j in range(cut))
    cycle = sum(b * base**j for j, b in enumerate(blocks[cut:]))
    return prefix + Fraction(base**cut * cycle, 1 - base**(len(blocks) - cut))


# Numerators of the four rotations of the virtual tail. Every admitted
# integer descends to this set, since its residue is a power of two mod 15.
BASE = {}
for i in range(4):
    rotation = TAIL[i:] + TAIL[:i]
    source = -integer(rotation)
    for mode in range(6):
        value = 15 * periodic_image(rotation, mode)
        assert value.denominator == 1
        BASE[source, mode] = value.numerator


def virtual_image(n, mode):
    """Apply one infinite-word carry to the numerator n over denominator 15."""
    assert n % 15 in (1, 2, 4, 8)
    low = width = 0
    while mode != -1 and (n, mode) not in BASE:
        bit = n % 2
        new, mode = H397.rules[mode][bit]
        low += (15 * new) << width
        width += 1
        n = (n - 15 * bit) // 2
    return low + ((n if mode == -1 else BASE[n, mode]) << width)


def scalar_step(n, power, mode):
    image = virtual_image(n, mode)
    if (image - n) % 15:
        return None
    if -7 * power <= image < 8 * power:
        return image, power
    for edge, corrected in enumerate(CORRECTED):
        if corrected is None:
            continue
        origin = EDGE[edge] * power
        if origin <= image < origin + 15 * power:
            return image + (corrected - EDGE[edge]) * power, power << len(H397.extension[edge])
    raise AssertionError('unclassified physical edge')


def encode(word):
    power = 1 << len(word)
    return 15 * integer(word) - 7 * power, power


def check():
    assert tuple(BASE[-7, m] for m in range(6)) == EDGE
    for m, extension in enumerate(H397.extension):
        if extension is not None:
            assert encode(extension)[0] == CORRECTED[m]
    # Each high 0111 nibble leaves exactly the same possible halting carries.
    assert {m for m in range(6) if sweep(H397, TAIL, m) is None} == {2, 4}
    assert all(sweep(H397, (1,) + TAIL, m) is not None for m in range(6))
    assert all(sweep(H397, (1,), m) is not None for m in range(6))
    for width in range(12):
        for word in product((0, 1), repeat=width):
            n, power = encode(word)
            for mode in range(6):
                actual = sweep(H397, word, mode)
                assert scalar_step(n, power, mode) == (None if actual is None else encode(actual))
                if actual is None:
                    assert n < 0
    # All shorter halting words 0(1110)^j approach 7/15 from below.
    for j in range(32):
        word = (0,) + TAIL * j
        assert sweep(H397, word, 0) is None
        assert encode(word)[0] == -14
    word = ()
    for _ in range(26):
        word = one_return(word)
    other = tuple(map(int, '100101011100000011010010001001100001'))
    assert ''.join(map(str, word)) == '101101011100010010000010001001100001'
    assert len(word) == len(other) == 36 and word[-16:] == other[-16:]
    assert word.count(0) == other.count(0) == 22
    assert encode(other)[0] - encode(word)[0] == 9_707_460
    assert register(word) == register(other) == (209, 9)
    assert register(word[1:]) == register(other[1:]) == (70, 9)
    for k in (1, 2, 3):
        assert sorted(word[i:i+k] for i in range(len(word)-k+1)) == sorted(
            other[i:i+k] for i in range(len(other)-k+1))
    for _ in range(44):
        other = one_return(other)
        assert other is not None
    for mode in RETURN[:7]:
        other = sweep(H397, other, mode)
        assert other is not None
    assert sweep(H397, other, RETURN[7]) is None


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    check()
    print('Verified the scalar guard, its sharp threshold, and the matched-register counterexample.')
