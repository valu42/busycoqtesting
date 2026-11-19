"""Exact finite checks used in the coarse jump-indicator entropy proof."""
from fractions import Fraction
from itertools import product

J = 4
PAIRS = ((5, 20), (9, 35), (7, 26), (7, 29))


def cost(symbol):
    return 1 if symbol == J else 2


def check_transport():
    for size in range(1, 6):
        for word in product(range(5), repeat=size):
            modulus = 3 ** sum(map(cost, word))
            fourth = pow(4, -1, modulus)

            def phase(k, e):
                q = 47
                for symbol in word:
                    if symbol == J:
                        k = (3*k-q) % modulus
                        e = (3*e+q-2*k) % modulus
                    else:
                        v, b = PAIRS[symbol]
                        k = 9*k*fourth % modulus
                        e = ((9*e+q*b)*fourth-k*v) % modulus
                return k, e

            def physical(u, d):
                for symbol in word:
                    if symbol == J:
                        d = (3*d-u+1) % modulus
                        u += 2
                    else:
                        v, b = PAIRS[symbol]
                        d = (9*d+b)*fourth % modulus
                        u += v
                return u % modulus, d

            # The formal linear coefficients of the two input variables vanish
            # modulo 3^m, as tested on an affine basis.
            assert phase(0, 0) == phase(1, 0) == phase(0, 1)
            u0, d0 = physical(0, 0)
            u1, d1 = physical(1, 0)
            assert (u1-u0) % modulus == 1
            assert physical(0, 1) == (u0, d0)
            u, d = physical(17, 31)
            assert (d-d0-(d1-d0)*(u-u0)) % modulus == 0

    # The inverse deviation maps preserve [-7,0] at every allowed slope.
    for x in (0, Fraction(1, 2)):
        for f in (-7, 0):
            assert -7 <= Fraction(f-1+2*x, 3) <= 0
            for v, b in PAIRS:
                assert -7 <= Fraction(4*(f+x*v)-b, 9) <= 0


def last_blocks(word, end, limit):
    start = end
    span = 0
    while span < limit:
        start -= 1
        span += cost(word[start])
    return start, span


def first_blocks(word, start, limit):
    end = start
    span = 0
    while span < limit:
        span += cost(word[end])
        end += 1
    return end


def check_contexts():
    # Identical short encodings must give identical ordered edges, even if
    # either history overshoots its requested length by one elementary call.
    m, ell, r = 3, 2, 5
    outer = {}
    inner = {}
    for body in product(range(5), repeat=7):
        word = (J,)*6 + body + (J,)*10
        coarse = tuple(1 if symbol == J else 0 for symbol in word)
        codes = tuple('1' if bit else '00' for bit in coarse)
        for cut in (7, 8, 9):
            pre, span = last_blocks(word, cut, m)
            after, _ = last_blocks(word, cut+1, m)
            end = first_blocks(word, cut, ell)
            next_end = first_blocks(word, cut+1, ell)
            labels = tuple(x for x in word[pre:cut+1] if x != J)
            assert 2*len(labels) <= m+3
            encoding = (''.join(codes[pre:])[:m+ell+4], span, labels)
            edge = (word[pre:cut], coarse[cut:end], word[cut],
                    word[after:cut+1], coarse[cut+1:next_end])
            assert outer.setdefault(encoding, edge) == edge

            start, span = last_blocks(word, cut, r)
            next_start, _ = last_blocks(word, cut+1, r)
            encoding = (''.join(codes[start:])[:r+3], span, labels)
            edge = (coarse[start:cut], word[pre:cut], word[cut],
                    coarse[next_start:cut+1], word[after:cut+1])
            assert inner.setdefault(encoding, edge) == edge
    return len(outer), len(inner)


def logarithm(x):
    """Rational lower and upper bounds from log x = 2 atanh((x-1)/(x+1))."""
    y = (x-1)/(x+1)
    assert 0 < y < 1
    terms = 28
    lower = sum(2*y**(2*i+1)/(2*i+1) for i in range(terms))
    error = 2*y**(2*terms+1)/((2*terms+1)*(1-y*y))
    return lower, lower+error


def check_bound():
    l2, u2 = logarithm(Fraction(2))
    l3, u3 = logarithm(Fraction(3))
    l15, u15 = logarithm(Fraction(3, 2))
    low = 1-u2/l3
    high = 1-l2/u3
    assert 0 < low < high
    c = low**2/(high*(1/l3+1/l15)+1/l3)
    upper = high**2/(low*(1/u3+1/u15)+1/u3)
    assert Fraction(63166175672, 10**12) < c < upper < Fraction(63166175674, 10**12)
    assert c > Fraction(1, 16)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    check_transport()
    counts = check_contexts()
    check_bound()
    print(f'Checked {counts[0]} outer and {counts[1]} inner context encodings.')
    print('The binary entropy lower bound lies between 0.063166175672 and 0.063166175674.')
