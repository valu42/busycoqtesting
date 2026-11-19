"""Check the line 596 proof identities, the first divergence and the halting family."""
from return596 import GUARDED, TARGET, cells, next_boundary


def step(table, ones, head, state):
    transition = table[2 * state + (head in ones)]
    assert transition is not None
    bit, direction, state = transition
    (ones.add if bit else ones.discard)(head)
    return head + direction, state


def cross(table, word, state, direction, result_word, result_state, result_dir, duration):
    head = 0 if direction == 1 else len(word) - 1
    tape = cells(word)
    for _ in range(duration):
        assert 0 <= head < len(word)
        head, state = step(table, tape, head, state)
    assert (head, state, tape) == (len(word) if result_dir == 1 else -1,
                                   result_state, cells(result_word))


def local_identities(table):
    # A=0, B=1, C=2, D=3. Exiting a finite window leaves its surroundings intact.
    rows = [
        ('0110110', 0, 1, '1010011', 1, 1, 9),
        ('1110', 1, 1, '0011', 1, 1, 4),
        ('1111', 1, 1, '1101', 0, -1, 9),
        ('0011', 0, -1, '1101', 0, -1, 6),
        ('0011', 2, -1, '1111', 2, -1, 4),
        ('1010011', 0, -1, '1101101', 0, -1, 17),
        ('1010011', 2, -1, '0111011', 3, -1, 17),
    ]
    for row in rows:
        cross(table, *row)
    # Blank -> P(2, empty) with initial head at position zero.
    ones = set()
    head = state = 0
    for _ in range(51):
        head, state = step(table, ones, head, state)
    assert state == 3 and ones == cells('01110111', head + 1)

    # P(n,x) -> L(0, 1^(n+4)x). Cells 6 onward are unexamined.
    ones = cells('011101')
    head, state = -1, 3
    for _ in range(60):
        assert head < 6
        head, state = step(table, ones, head, state)
    assert head == -5 and state == 0 and ones == cells('1101101111', head + 1)


def comparison_guard():
    n, x, total = 2, '', 51
    for i in range(1, 176):
        if i == 10:
            assert (n, x) == (306, '010111')
        if i == 175:
            assert (n, x, total) == (139072280281797265838838, '01101011',
                                     13815070816270554710970280936463660063164325600)
        kind, a, b, dt = next_boundary(n, x, GUARDED)
        total += dt
        if i < 175:
            assert kind == 'P'
            assert next_boundary(n, x, TARGET) == (kind, a, b, dt)
        else:
            assert kind == 'halt' and total == 24560125895592097263948984175956746215829548953
            real = next_boundary(n, x, TARGET)
            assert real[0] == 'P'
        n, x = a, b


def halting_family():
    residues = '111111111111111211110111111011212102'
    n0, modulus = 44932349626276, 150094635296999121
    assert modulus == 3 ** len(residues)
    n, x, time = n0, '', 0
    for j, symbol in enumerate(residues):
        r = int(symbol)
        assert n >= 300 and n % 3 == r
        kind, value, word, _ = next_boundary(300 + r, x, clock=False, affine=True)
        actual, a, b, dt = next_boundary(n, x)
        time += dt
        assert actual == kind
        if j + 1 == len(residues):
            assert kind == 'halt' and x == '011010101011'
            assert time == 1427510327116636722563042017802061340
        else:
            assert kind == 'P' and (a, b) == (4 * (n // 3) + value - 400, word)
            n, x = a, b


if __name__ == '__main__':
    local_identities(TARGET)
    local_identities(GUARDED)
    comparison_guard()
    halting_family()
    from shortest596 import shortest
    rows, words, _, classes = shortest()
    assert (rows, words, len(classes), classes[0]) == (1959, 774, 128, 44932349626276)
    print('Verified local crossings, blank initialization, first failed comparison and 36-return halting family.')
