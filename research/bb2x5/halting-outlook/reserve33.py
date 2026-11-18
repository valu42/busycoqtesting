"""Independent checks for the shifted canonical safety theorem, Python 3.10+."""
import base64
from itertools import product
import json
from pathlib import Path
import zlib

from neglected33 import CYCLE, MACHINE, batch, concrete, literal_step

PAIRS = ('22', *CYCLE)
CAP = '421'


def advance_pair(pair, count):
    if pair == '22':
        return pair, 2 * count
    phase = CYCLE.index(pair)
    tours, extra = divmod(count, 3)
    calls = tours + sum((phase + i) % 3 == 0 for i in range(extra))
    return CYCLE[(phase + extra) % 3], calls


def shift_one(outer, digit, inner, pair):
    """Emit one normalized pair. Precondition: at least one outer request."""
    assert outer > 0
    normalized, forwarded = advance_pair(pair, inner)
    x, y = normalized
    if digit == '2':
        initial, pending = '2' + x, outer
    elif digit == '1':
        initial, pending = '2' + x, outer - 1
    elif x == '1':
        initial, pending = '22', outer - 1
    else:
        initial, pending = ('21' if y == '1' else '22'), outer - 1
        carry, additional = {'1': ('4', 1), '2': ('2', 2), '4': ('1', 0)}[y]
        emitted, calls = advance_pair(initial, pending)
        return emitted, calls, carry, forwarded + additional
    emitted, calls = advance_pair(initial, pending)
    return emitted, calls, y, forwarded


def check_fixed_prefix():
    path = Path(__file__).with_name('neglected33-checkpoint.json')
    saved = json.loads(path.read_text())
    assert saved['machine'] == MACHINE and saved['left_extension'] == 33
    tape = zlib.decompress(base64.b64decode(saved['word_zlib_base64'])).decode()
    # At a left extension the tape is 2y. At 33, y is 2 followed by the register.
    assert tape.startswith('22')
    flux, carry, inner = 1, '2', 0
    ternary = []
    for j in range(7243):
        pair = tape[2 + 2*j:4 + 2*j]
        emitted, next_flux, next_carry, next_inner = shift_one(flux, carry, inner, pair)
        if j == 7242:
            assert pair == '14' and emitted == '22'
            assert (flux.bit_length(), carry, inner.bit_length()) == (7237, '2', 7177)
            break
        assert pair == emitted and flux > 0
        old_load = flux + inner - (carry == '1')
        new_load = next_flux + next_inner - (next_carry == '1')
        if pair == '22':
            assert new_load == 2 * old_load
        else:
            ternary.append((j, pair))
            assert 3 * new_load == old_load + 2
        flux, carry, inner = next_flux, next_carry, next_inner
    assert ternary == [(62, '14'), (3078, '24')]


def main():
    check_fixed_prefix()
    rows = 0
    for pair, digit, inner, outer, suffix in product(
            PAIRS, '124', range(6), range(1, 7), ('', '21', CAP, '22' + CAP)):
        p, n, d, s = shift_one(outer, digit, inner, pair)
        left_inner = batch(pair + suffix, inner)[0]
        left = batch(digit + left_inner, outer)[0] if suffix.endswith(CAP) else None
        if left is not None:
            right_inner = batch(suffix, s)[0]
            assert left == p + batch(d + right_inner, n)[0]
            rows += 1

    reachable = {(d, 0) for d in '124'}
    while True:
        successors = {shift_one(1, d, s, q)[2:] for d, s in reachable for q in CYCLE}
        if successors <= reachable:
            break
        reachable |= successors
    assert reachable == {('1', 0), ('2', 0), ('4', 0), ('4', 1)}

    for digit, inner, outer in product('124', range(7), range(1, 7)):
        assert shift_one(outer, digit, inner, '22')[0] == '22'
    for digit, inner in sorted(reachable):
        allowed = '14' if digit != '4' else ('21' if inner == 0 else '24')
        for outer in range(1, 7):
            assert [t for t in CYCLE if shift_one(outer, digit, inner, t)[0] != '22'] == [allowed]

    cases = 0
    for length in range(4):
        for pieces in product(PAIRS, repeat=length):
            for digit, n, r in product('124', (0, 1, 2, 3, 8, 67, 702), range(1, 4)):
                word = digit + ''.join(pieces) + CAP * r
                result, cost = batch(word, n)
                # Stronger identity than a terminal-block count. Delete all but
                # one block at the start and reinsert exactly those after replay.
                trimmed = digit + ''.join(pieces) + CAP
                prefix, cost_one = batch(trimmed, n)
                assert result == prefix + CAP * (r - 1)
                assert cost == cost_one + 3 * (r - 1) * (len(prefix) - len(trimmed))
                cases += 1
    virgin20 = batch('', 20)[0]
    assert batch('', 40)[0] == '21' * 4
    for r in range(1, 8):
        prior = batch(virgin20 + CAP * r, 20)[0]
        result = batch('2' + prior, 2)[0]
        assert result == '22' * 4 + virgin20 + CAP * (r - 1)
    calibration_tape = concrete('2' + '21' * 4)
    head, state = 0, 'A'
    for _ in range(347):
        assert head >= 0
        head, state = literal_step(calibration_tape, head, state)
    assert (head, state, calibration_tape) == (-1, 'B', concrete(CAP * 10))
    virgin4 = batch('', 4)[0]
    for r in range(1, 8):
        prior = batch(virgin4 + CAP * r, 4)[0]
        assert batch('2' + prior, 4)[0] == '14' + '22' * 2 + virgin4 + CAP * (r - 1)
    prior = batch('2' + batch(virgin4, 4)[0], 3)[0]
    tape = concrete(prior)
    head, state = 0, 'A'
    for _ in range(137):
        assert head >= 0
        head, state = literal_step(tape, head, state)
    assert state == 'B' and tape[head] == 3
    word = '2221421'
    for expected in ('222242421421', '2222222222414211421'):
        word = '2' + batch(word, 4)[0]
        assert word == expected
    tape = concrete(word)
    head, state = 0, 'A'
    for _ in range(203):
        assert head >= 0
        head, state = literal_step(tape, head, state)
    assert (head, state, tape[head]) == (13, 'B', 3)
    print(f'{rows} shift identities, {len(reachable)} residual states, {cases} shifted batches')


if __name__ == '__main__':
    main()
