"""Prove finite F identities by rewriting expressions with an uninterpreted suffix x."""


def normal(term):
    # Symbols are unary functions, so F01x means F(0(1(x))).
    i = len(term)
    while i:
        i -= 1
        if term[i] != 'F':
            continue
        start = i + 1
        pos = start
        while term.startswith('1001', pos):
            pos += 4
        length = pos - start
        if term.startswith('0', pos):
            out, end = '1' * (length + 1), pos + 1
        elif term.startswith('11', pos):
            out, end = '0' * length + '11F', pos + 2
        elif term.startswith('101', pos):
            out, end = '0' * length + '111', pos + 3
        elif term.startswith('1000', pos) and term[pos+4:pos+5] in ('0', '1'):
            out, end = '0' * length + '00011', pos + 5
        else:
            continue
        term = term[:i] + out + term[end:]
        i += len(out)
    return term


def identity(n, left, right, calls, shifted=False):
    lhs = 'F' * n + left + 'x'
    if shifted:
        assert right.endswith('1')
        rhs = right[:-1] + 'F' * (2 * calls) + '1x'
    else:
        rhs = right + 'F' * calls + 'x'
    assert normal(lhs) == normal(rhs), (lhs, rhs, normal(lhs), normal(rhs))


def verify_identities():
    # Q(s,1x). Base F^2 on 000111, then add four pulses per unit increase in s.
    identity(2, '000111', '000011', 1)
    identity(4, '000011', '000011', 1)

    # Q(s,0001111x), base s=2. The extra pulses as s increases by two
    # preserve each output prefix and add exactly the tail calls shown.
    identity(6, '000110001111', '000000001111', 1)
    identity(8, '000000001111', '000000001111', 1)
    identity(14, '00000001111', '00011000111', 1, shifted=True)
    identity(16, '00011000111', '00011000111', 1, shifted=True)
    identity(30, '0011000111', '1111000111', 7)
    identity(32, '1111000111', '1111000111', 8)
    identity(1, '11000111', '11100111', 0)
    identity(1, '100111', '000011', 1)

    # Q(s,0010000b1x). Four exceptional returns follow the first sweep.
    for bit in '01':
        identity(6, '00011' + '0010000' + bit + '1', '11111111100011', 1)
    identity(4, '11111111100011', '11111111100011', 1)
    identity(1, '111111100011', '111111000111', 0)
    identity(1, '1111000111', '1111100111', 0)
    identity(1, '11100111', '11000011', 1)
    identity(1, '000011', '100011', 0)


if __name__ == '__main__':
    verify_identities()
    print("All identities hold with x left arbitrary.")
