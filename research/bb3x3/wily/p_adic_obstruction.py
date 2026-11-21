"""Constructive all-depth obstruction to fixed P-adic residue invariants.

P=1+z+z^2 over F2, t=1/(1+z^2). For every k>=1 and M>=1,
construct an immediately halting word with the same completed-series residue
mod P^k, suffix11, and length modulo M as a reachable blank-core word.
"""
from math import lcm
from certificates import pass_word

P = 0b111
TAIL_DEN = 0b101
TARGET_INDEX = 90
TARGET = '01101011100010010111'


def mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def divide(a, b):
    quotient = 0
    while a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        quotient ^= 1 << shift
        a ^= b << shift
    return quotient, a


def mod(a, b):
    return divide(a, b)[1]


def power(a, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent >>= 1
    return result


def inverse(a, modulus):
    r0, r1, s0, s1 = modulus, a, 0, 1
    while r1:
        quotient, remainder = divide(r0, r1)
        r0, r1 = r1, remainder
        s0, s1 = s1, s0 ^ mul(quotient, s1)
    assert r0 == 1
    return mod(s0, modulus)


def word_polynomial(word):
    return sum(int(bit) << i for i, bit in enumerate(word))


def completion_numerator(word):
    return mul(TAIL_DEN, word_polynomial(word)) ^ (1 << len(word))


def construct(k, length_modulus=1):
    assert k >= 1 and length_modulus >= 1
    target_numerator = completion_numerator(TARGET)
    quotient, remainder = divide(target_numerator ^ TAIL_DEN, P)
    assert remainder == 0
    h = power(P, k - 1)
    # (z^3+1)^(2^e)=(z+1)^(2^e) P^(2^e), hence z^L=1 modh.
    e = (max(1, k - 1) - 1).bit_length()
    period = lcm(3 * (1 << e), length_modulus, 2)
    if h != 1:
        assert mod(1 << period, h) == 1
        residual = mod(mul(inverse(TAIL_DEN, h), quotient ^ (1 << 19))
                       ^ (1 << 16), h)
    else:
        residual = 0
    # Move each monomial by a multiple of period, separating every pair.
    exponents = [i + (i + 1) * period
                 for i in range(residual.bit_length()) if residual >> i & 1]
    top = max(exponents, default=-1)
    copies = max(0, (top + 8 - 19 + period - 1) // period)
    cut = 19 + copies * period
    assert cut > top + 7 and cut % 2 == 1
    # A final isolated1 ensures the input word ends1111, hence inparticular11.
    exponents.append(cut - 3)
    q = sum(1 << exponent for exponent in exponents)
    assert q & (q << 1) == 0
    # Y=Q+z^cut/TAIL_DEN hasno11. X=P Y+1=W+z^(cut+1)/TAIL_DEN.
    w_polynomial = mul(P, q) ^ 1 ^ (1 << cut)
    word = ''.join(str(w_polynomial >> i & 1) for i in range(cut + 1))
    assert word.endswith('11')
    assert len(word) % length_modulus == len(TARGET) % length_modulus
    assert mod(completion_numerator(word) ^ target_numerator, power(P, k)) == 0
    assert pass_word(word) is None
    return word


def verify():
    actual = '001100'
    for _ in range(TARGET_INDEX):
        actual = pass_word(actual)
        assert actual is not None
    assert actual == TARGET
    records = []
    for k in range(1, 13):
        for modulus in (1, 2, 3, 5, 8, 11):
            word = construct(k, modulus)
            records.append({'k': k, 'length_modulus': modulus,
                            'witness_length': len(word),
                            'witness_ones': word.count('1')})
    return {'status': 'verified; all-k theorem is proved in the note',
            'target_index': TARGET_INDEX, 'target_word': TARGET,
            'example_k1': construct(1), 'example_k2': construct(2),
            'finite_regression_checks': records}


if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2))
