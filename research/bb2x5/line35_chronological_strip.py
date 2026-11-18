"""Check interval, left-prefix and altered-tape certificates for BB(2,5) line 35."""

import argparse
import base64
import json
import zlib
from collections import Counter
from itertools import product
from pathlib import Path

from frontiers.checkpoints import checksum
from line35_guard_stream import (
    ALPHABET, CLOSE, OPEN, balance, debt_of, deficit, match_letters,
    packed_successor, physical_digit, prefix_successor, unpack,
)
from line35_pascal import normalized35
from line37_orbit import encode, match
from line37_stream import run_cell
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch, word_sweep


HEIGHT = 5
# Letters 0 and 1 have zero debt, 2 has unit debt, and 3 includes every debt >= 2.
LETTERS = range(4)
BLOCK = tuple(map(int, '3313333333133111111'))
FOOT = tuple(map(int, '1211212'))


def cell(symbol, letter):
    """One exact fixed-right-index column sample, in physical line 35 digits."""
    debt = max(0, letter - 1)
    survivor = symbol == OPEN and debt == 0
    outgoing = max(0, debt + (symbol == CLOSE) - (symbol == OPEN))
    return physical_digit(survivor, letter == 1), outgoing + 1 if outgoing else int(survivor)


def cross(interface, symbol, saturate):
    """Read one spatial column through all five times."""
    choices = [()]
    rows = [symbol]
    for incoming in interface:
        next_symbol, emitted = cell(symbol, incoming)
        outputs = (emitted,)
        if saturate:
            # Only an opening can take the high class back down to unit debt.
            if symbol == OPEN and incoming == 3:
                outputs = (2, 3)
            else:
                outputs = (min(3, emitted),)
        choices = [prefix + (y,) for prefix in choices for y in outputs]
        rows.append(next_symbol)
        symbol = next_symbol
    return rows, choices


def make_graph():
    for symbol in ALPHABET:
        for letter in range(10):
            next_symbol, emitted = cell(symbol, letter)
            (shared,) = normalized35((symbol,))
            (shared_next,) = normalized35((next_symbol,))
            assert run_cell(shared, letter) == (shared_next, emitted)
            rows, targets = cross((min(3, letter),), symbol, True)
            assert rows[-1] == next_symbol and (min(3, emitted),) in targets
    vertices = list(product(LETTERS, repeat=HEIGHT))
    ids = {vertex: i for i, vertex in enumerate(vertices)}
    edges = []
    for vertex in vertices:
        outgoing = []
        for symbol in ALPHABET:
            rows, targets = cross(vertex, symbol, True)
            weights = tuple((q == OPEN) - (q == CLOSE) for q in rows)
            outgoing.extend((ids[t], weights) for t in targets)
        edges.append(outgoing)
    assert (len(edges), sum(map(len, edges))) == (1024, 6818)
    return edges


def certify_cost(edges, coefficients, constant, floor):
    """Find a potential, then check its inequality on every edge directly."""
    costs = [[(j, constant + sum(a * w for a, w in zip(coefficients, weights)))
              for j, weights in outgoing] for outgoing in edges]
    potential = [0] * len(edges)
    for _ in range(len(edges)):
        changed = False
        for i, outgoing in enumerate(costs):
            for j, cost in outgoing:
                candidate = potential[i] + cost
                if potential[j] > candidate:
                    potential[j] = candidate
                    changed = True
        if not changed:
            break
    assert all(potential[j] <= potential[i] + cost
               for i, outgoing in enumerate(costs) for j, cost in outgoing)
    assert (min(potential), max(potential)) == (-floor, 0)
    print('row coefficients', coefficients, 'length coefficient', constant, 'lower bound', -floor)


def length_envelope(edges):
    # v_L(j) is the smallest last-row balance for L arbitrary edges ending at j.
    simple = [[(j, weights[-1]) for j, weights in outgoing] for outgoing in edges]
    vectors = [[0] * len(edges)]
    for length in range(1, 87):
        following = [length + 1] * len(edges)
        for i, outgoing in enumerate(simple):
            for j, weight in outgoing:
                following[j] = min(following[j], vectors[-1][i] + weight)
        assert max(following) <= length
        vectors.append(following)
    assert all(b == a - 2 for a, b in zip(vectors[67], vectors[86]))
    extrema = [min(v) for v in vectors]
    first = [next(length for length, value in enumerate(extrema) if value <= -debt)
             for debt in range(1, 13)]
    assert first == [1, 3, 8, 13, 18, 29, 37, 48, 56, 67, 75, 86]
    print('all 1024 endpoint values at length 86 equal those at 67 minus two')
    print('least graph widths at deficits 1 through 12:', *first)

    # For debts above twelve the first possible length is above 86, so the
    # endpoint-vector identity gives w(d+2) = w(d)+19 indefinitely.
    def minimum_width(debt):
        if debt <= 12:
            return first[debt - 1]
        base = 11 if debt % 2 else 12
        return first[base - 1] + 19 * ((debt - base) // 2)

    five_widths = []
    for debt in (2, 3, 4, 5, 6):
        length = minimum_width(debt)
        widths = [length]
        for _ in range(4):
            openings = length - 1
            length = openings + minimum_width(openings + debt)
            widths.append(length)
        five_widths.append(widths[-1])
        print('minimum necessary widths for successive readings at least', debt, ':', *widths)
    assert five_widths == [14973, 84431, 157195, 230304, 376148]


def check_debt_witnesses():
    checked = 0
    for length in range(2, 9):
        for body in product(ALPHABET, repeat=length - 1):
            word = body + (CLOSE,)
            new, _ = word_sweep(word, TERNARY_CLOSE)
            if new is None:
                continue
            letters = match_letters(word)
            for left in range(length - 1):
                debt = debt_of(letters[length - left - 1])
                if debt == 0:
                    continue
                b = 0
                for end in range(left, length):
                    b += (word[end] == OPEN) - (word[end] == CLOSE)
                    if b == -debt:
                        break
                assert b == -debt
                assert all(letters[length - i - 1] != 1 for i in range(left, end + 1))
                offset = len(new) - length
                assert all(q == OPEN for q in new[left + offset:end + offset])
                checked += 1
    print('right-index opening runs after positive debt:', checked, 'word/cut cases')


def check_packed_prefixes():
    # Compare the bit update used by the large closure with two word-level paths.
    for n in range(5, 8):
        for prefix in product(ALPHABET, repeat=n):
            opens, closes = encode(normalized35(prefix))
            survivors, internal, _ = match(n, opens, closes, n)
            count = survivors.bit_count()
            for incoming in range(6 + balance(prefix) + 1):
                actual, _ = word_sweep(prefix + (CLOSE,) * incoming + (OPEN, CLOSE), TERNARY_CLOSE)
                guard = internal + max(0, incoming - count)
                predicted = prefix_successor(prefix, incoming)
                if guard >= 6:
                    assert predicted is None and actual is None
                else:
                    width, o, c = packed_successor(n, survivors, guard)
                    clipped = unpack(n, o >> (width - n), c >> (width - n))
                    assert clipped == predicted == tuple(actual[:n])
                survivors &= survivors - 1


def check_left_cut():
    machine = TapeMachine(TERNARY_CLOSE)
    for _ in range(15):
        seed = direct_epoch(machine, ALPHABET)
    assert ''.join(map(str, seed)) == '13111231121113111111112113112'
    n = 28
    mask = (1 << n) - 1
    o, c = encode(normalized35(seed[:n]))
    first = (o << n) | c
    queue = [first]
    seen = {first}
    histogram = Counter()
    successful = 0
    for state in queue:
        opens, closes = state >> n, state & mask
        survivors, internal, _ = match(n, opens, closes, n)
        assert internal <= 5
        histogram[internal] += 1
        count = survivors.bit_count()
        for incoming in range(count + 6 - internal):
            guard = internal + max(0, incoming - count)
            width, o, c = packed_successor(n, survivors, guard)
            shift = width - n
            successor = ((o >> shift) << n) | (c >> shift)
            if successor not in seen:
                seen.add(successor)
                queue.append(successor)
            survivors &= survivors - 1
            successful += 1
    assert (len(seen), successful) == (711_940, 12_856_742)
    assert [histogram[i] for i in range(6)] == [343615, 231841, 135257, 1083, 135, 9]
    print('cut 28:', len(seen), 'prefixes;', successful, 'successful prefix/debt inputs')
    print('prefix counts by internal deficit 0 through 5:', *(histogram[i] for i in range(6)))

    # Each successful transition has a literal realization with this chosen tail.
    # The tails are chosen afresh, so the path alone has no blank reachability claim.
    prefix = tuple(seed)
    for incoming in (19, 0, 25, 0, 19, 0, 10, 0, 4, 0):
        expected = prefix_successor(prefix, incoming)
        tape = prefix + (CLOSE,) * incoming + (OPEN, CLOSE)
        actual = direct_epoch(TapeMachine(TERNARY_CLOSE, tape, left=1), ALPHABET)
        assert expected is not None and expected == tuple(actual[:29])
        prefix = expected
    assert deficit(prefix) == 6 and deficit(prefix[:28]) == 5
    print('cut 29: ten individually realized exterior choices give first internal deficit six at cell 29')


def check_control():
    # Rightmost C emits letter 2 forever. Walk left to the foot/block seam.
    seam = (2,) * HEIGHT
    for q in reversed(FOOT[:-1]):
        _, (seam,) = cross(seam, q, False)
    assert seam == (0, 0, 1, 0, 1)
    interface = seam
    rows = [[] for _ in range(HEIGHT + 1)]
    for q in reversed(BLOCK):
        digits, (interface,) = cross(interface, q, False)
        for row, digit in zip(rows, digits):
            row.append(digit)
    assert interface == seam
    rows = [tuple(reversed(r)) for r in rows]
    assert [balance(row) for row in rows] == [8, 10, 13, 7, 7, -2]
    assert ''.join(map(str, rows[-1])) == '3123231232312323112'

    # Two copies suffice. Recover both boundaries around the translated blocks
    # on every row and check the prefix inequality for every multiplicity.
    seed = BLOCK * 2 + FOOT
    machine = TapeMachine(TERNARY_CLOSE, seed, left=1)
    word = list(seed)
    shift = 0
    guards = []
    prefix_floors = []
    for i, block in enumerate(rows):
        assert tuple(word[shift:shift + 2 * len(block)]) == block * 2
        actual, low = word_sweep(word, TERNARY_CLOSE)
        assert actual == direct_epoch(machine, ALPHABET)
        guards.append(-low)
        if i < HEIGHT:
            left = tuple(word[:shift])
            right = tuple(word[shift + 2 * len(block):])
            # The block has nonnegative adjusted total, so it suffices to test
            # its first copy and the smallest allowed multiplicity at the foot.
            assert 3 * balance(block) >= len(block)
            test = left + block * 2 + right
            b = 0
            floor = 0
            for j, q in enumerate(test, 1):
                b += (q == OPEN) - (q == CLOSE)
                floor = min(floor, 3*b - j)
            prefix_floors.append(floor)
            assert actual is not None
            shift += len(actual) - len(word)
            word = actual
    assert guards == [0, 1, 0, 1, 0, 6] and prefix_floors == [-7, -8, 0, -7, 0]
    assert (machine.steps, machine.head, machine.state, machine.tape[machine.head]) == (1233, -7, 'B', 4)
    print('19-cell return balances:', *(balance(r) for r in rows))
    print('45-cell altered tape guards:', *guards, 'defined instructions:', machine.steps, 'head:', machine.head)
    print('five prefix floors for 3b(P)-length:', *prefix_floors)


def check_blank_copies(start, delay, right, left, expected_block, expected_history, extra):
    """Duplicate a single genuine interval before the point where its balance drops."""
    word = []
    for _ in range(start):
        word, _ = word_sweep(word, TERNARY_CLOSE)
        assert word is not None
    seed = tuple(word)
    a, b = len(seed) - 1 - left, len(seed) - 1 - right
    block = seed[a:b]
    assert ''.join(map(str, block)) == expected_block
    history = []
    guards = []
    for _ in range(delay):
        letters = match_letters(word)
        assert letters[left] == letters[right]
        history.append(letters[left])
        word, low = word_sweep(word, TERNARY_CLOSE)
        assert word is not None
        guards.append(-low)
    assert tuple(history) == expected_history
    a_end, b_end = len(word) - 1 - left, len(word) - 1 - right
    left_balance = balance(word[:a_end])
    assert deficit(word[:a_end]) < 6
    loss = -balance(word[a_end:b_end])
    one = debt_of(match_letters(word)[left])
    assert loss > 0 and extra == (6 + left_balance - one + loss - 1) // loss
    real_successor, _ = word_sweep(word, TERNARY_CLOSE)
    assert real_successor is not None

    for copies in (extra - 1, extra):
        altered = seed[:a] + block * (copies + 1) + seed[b:]
        machine = TapeMachine(TERNARY_CLOSE, altered, left=1)
        for guard in guards:
            altered, low = word_sweep(altered, TERNARY_CLOSE)
            assert altered is not None and -low == guard
            assert direct_epoch(machine, ALPHABET) == altered
        final, low = word_sweep(altered, TERNARY_CLOSE)
        assert final == direct_epoch(machine, ALPHABET, limit=2_000_000)
        assert (final is None) == (copies == extra)
        if final is None:
            assert (machine.state, machine.tape[machine.head]) == ('B', 4)
        print('blank epoch', start, 'plus', copies, 'extra copies of', expected_block,
              'agrees for', delay, 'sweeps; next debt', -low, 'defined instructions', machine.steps)


def check_left_fifth():
    width, opens, closes = 1, 0, 1
    last_miss = least_after = None
    for epoch in range(1, 40_001):
        survivors, guard, _ = match(width, opens, closes, width)
        assert guard < 6
        cut = (width + 4) // 5
        if cut >= 25:
            o, c = opens >> (width - cut), closes >> (width - cut)
            _, internal, _ = match(cut, o, c, cut)
            margin = 2 * cut + 19 * (o.bit_count() - c.bit_count()) - 2 * width + 58
            if internal > 5 or margin < 0:
                last_miss, least_after = epoch, None
            elif least_after is None or margin < least_after[0]:
                least_after = (margin, epoch)
        width, opens, closes = packed_successor(width, survivors, guard)
    assert (last_miss, least_after) == (593, (111, 597))
    print('left-fifth test: last miss 593; epochs 594 through 40000 pass; least margin 111 at 597')


def check_odd_checkpoint(path):
    """Find the shortest prefix satisfying the linear test at a saved odd epoch."""
    doc = json.loads(path.read_text())
    record = doc['payload']
    if (doc['sha256'] != checksum(record) or record['format'] != 'bb2x5-line35-epoch-v1'
            or record['machine'] != TERNARY_CLOSE or record['state'] != 'A'
            or record['epoch'] < 11 or record['epoch'] % 2 != 1
            or record['left'] != record['head'] + 1):
        raise ValueError('expected a verified-format line 35 odd-epoch checkpoint')
    word = zlib.decompress(base64.b64decode(record['tape_zlib_base64'], validate=True))
    assert len(word) == record['cells'] and word[-2:] == bytes((OPEN, CLOSE))
    assert set(word) <= set(ALPHABET)
    triples = 0
    for j in range(2, len(word) - 2, 3):
        if word[-1-j] != OPEN or word[-3-j] != OPEN:
            break
        triples += 1
    assert triples >= 1
    uncovered = len(word) - 3 * triples
    b = h = 0
    for cut, symbol in enumerate(word[:uncovered], 1):
        b += (symbol == OPEN) - (symbol == CLOSE)
        h = max(h, -b)
        margin = 2*cut + 19*b - 2*uncovered + 54
        if cut >= 25 and h <= 5 and margin >= 0:
            print('checkpoint epoch', record['epoch'], 'zero-debt suffix', 3*triples,
                  'left width', uncovered, 'first sufficient cut', cut,
                  'balance', b, 'internal deficit', h, 'margin', margin)
            return
    print('no prefix meets the linear test at checkpoint epoch', record['epoch'])


def main():
    listed = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
    assert listed[34] == TERNARY_CLOSE == '1RB2LA4RA1LA3LA_0LA3RB3LB2RB---'
    edges = make_graph()
    print('five-time interfaces:', len(edges), 'vertices and', sum(map(len, edges)), 'labelled edges')
    # Chronological order, from the unconstrained oldest row to the newest.
    bounds = (
        ((0, 0, 0, 0, 0, 19), 2, 59),
        ((0, 0, 0, 0, 19, 19), -5, 71),
        ((0, 0, 0, 19, 0, 19), -5, 65),
        ((0, 0, 11, 0, 0, 11), -1, 45),
        ((0, 11, 0, 0, 0, 11), -4, 83),
        ((0, 0, 1, 1, 1, 1), -1, 5),
    )
    for coefficients, constant, floor in bounds:
        certify_cost(edges, coefficients, constant, floor)
    length_envelope(edges)
    check_debt_witnesses()
    check_control()
    check_packed_prefixes()
    check_left_cut()
    check_blank_copies(83, 4, 143, 153, '1231111112', (0, 1, 0, 1), 3)
    check_blank_copies(903, 15, 1699, 1722, '1' * 22 + '3', (1,) * 15, 93)
    check_left_fifth()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--odd-checkpoint', type=Path, help='also evaluate a saved odd-epoch blank word')
    args = parser.parse_args()
    main()
    if args.odd_checkpoint:
        check_odd_checkpoint(args.odd_checkpoint)
