"""Exact guard and chronological-column certificates for blank BB(2,5) line 35."""

from collections import Counter
from itertools import product
from pathlib import Path

from line35_pascal import normalized35
from line37_orbit import encode, match
from line37_pascal import column_pass
from line37_stream import Stream, cell_image, run_cell
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch, word_sweep


# Physical line 35 digits, left to right. The virtual bit precedes the old body.
OPEN, CLOSE, NEUTRAL = 1, 2, 3
HEADERS = ((2,), (1,), (3,), (1, 3, 2, 3), (1, 3, 1, 3), (1, 3, 3, 1))
VIRTUAL = (1, 1, 0, 0, 0, 0)
ALPHABET = (OPEN, CLOSE, NEUTRAL)
FIRST_STREAM = Stream((), (2,))
HEADER_MASKS = tuple(encode(normalized35(header)) for header in HEADERS)


def debt_of(letter):
    return max(0, letter - 1)


def balance(word):
    return word.count(OPEN) - word.count(CLOSE)


def deficit(word):
    height = maximum = 0
    for symbol in word:
        height += (symbol == CLOSE) - (symbol == OPEN)
        maximum = max(maximum, height)
    return maximum


def match_letters(word, incoming=0):
    """Letters for the physical cells, in order from the right edge."""
    letters = []
    for symbol in reversed(word):
        survives = symbol == OPEN and incoming == 0
        incoming = max(0, incoming + (symbol == CLOSE) - (symbol == OPEN))
        letters.append(incoming + 1 if incoming else int(survives))
    return letters


def physical_digit(left, right):
    return OPEN if left == right else CLOSE if right else NEUTRAL


def prefix_successor(prefix, incoming):
    letters = match_letters(prefix, incoming)
    guard = debt_of(letters[-1])
    if guard >= 6:
        return None
    survivors = [letter == 1 for letter in reversed(letters)]
    preceding = [VIRTUAL[guard]] + survivors[:-1]
    body = tuple(physical_digit(l, r) for l, r in zip(preceding, survivors))
    return (HEADERS[guard] + body)[:len(prefix)]


def birth_columns(letter):
    """New right-indices in increasing order, in the shared transducer's roles."""
    guard = debt_of(letter)
    first = physical_digit(VIRTUAL[guard], letter == 1)
    return normalized35((first,) + HEADERS[guard][::-1])


def next_stream(stream):
    first = stream.first()
    if debt_of(first) >= 6:
        return None
    stream = stream.drop_first()
    for symbol in birth_columns(first):
        stream = cell_image(stream, symbol)
    return stream


def threshold_after_history(history):
    """Follow a fixed old column. Return its exact dangerous next debt.

    A zero threshold means the new strip itself will halt. None means that a
    preceding sample already caused a halt. An empty new strip has threshold 6.
    """
    strip = []  # normalized digits, in order from the old column toward the guard
    for letter in history:
        for i, symbol in enumerate(strip):
            strip[i], letter = run_cell(symbol, letter)
        if debt_of(letter) >= 6:
            return None
        strip.extend(birth_columns(letter))
    physical = normalized35(reversed(strip))
    return 0 if deficit(physical) >= 6 else 6 + balance(physical)


def canonical_replay(prefix, incoming):
    # The final OC is balanced and has the real terminal symbol.
    word = prefix + (CLOSE,) * incoming + (OPEN, CLOSE)
    concrete = TapeMachine(TERNARY_CLOSE, word, left=1)
    actual = direct_epoch(concrete, ALPHABET)
    sweep, low = word_sweep(word, TERNARY_CLOSE)
    assert actual == sweep
    if actual is None:
        assert low == -6 and (concrete.state, concrete.tape[concrete.head]) == ('B', 4)
    return actual, low


def check_prefix_graph(seed):
    start = tuple(seed[:8])
    prefixes = [start]
    seen = {start}
    histogram = Counter()
    edges = set()
    vulnerable = set()
    successful = 0
    for prefix in prefixes:
        threshold = 6 + balance(prefix)
        histogram[threshold] += 1
        if threshold == 5:
            vulnerable.add(''.join(map(str, prefix)))
        assert deficit(prefix) <= 2
        for incoming in range(threshold + 1):
            guard = max(deficit(prefix), incoming - balance(prefix))
            assert debt_of(match_letters(prefix, incoming)[-1]) == guard
            actual, low = canonical_replay(prefix, incoming)
            predicted = prefix_successor(prefix, incoming)
            if incoming == threshold:
                assert predicted is None and actual is None
                continue
            assert predicted == tuple(actual[:8]) and low == -guard
            successful += 1
            edges.add((prefix, predicted))
            if predicted not in seen:
                seen.add(predicted)
                prefixes.append(predicted)
    assert [histogram[n] for n in range(5, 14)] == [4, 6, 5, 24, 6, 13, 9, 2, 2]
    assert vulnerable == {'21323213', '21323231', '23213123', '13232312'}
    assert (len(prefixes), successful, len(edges)) == (71, 616, 561)
    print('Cut 8: 71 prefixes, 616 successful inputs, 561 distinct edges; 71 first-failure B4 replays.')
    print('Prefix counts at debt thresholds 5 through 13:', *(histogram[n] for n in range(5, 14)))


def check_pascal_tails():
    # In this local table the shared code uses 2 for opening and 1 for closing.
    for previous, center in product((1, 2, 3), repeat=2):
        clean = (2, center, 2)
        even = column_pass(clean, previous != 1, 0)
        odd_input = int(previous != 1)
        even_input = 2 if previous == 3 else int(previous == 2)
        for triple, letter in ((clean, odd_input), (even, even_input)):
            for symbol in triple:
                _, letter = run_cell(symbol, letter)
                assert letter <= 2
    print('Pascal tails: debt at most 1 at every cell in all 9 adjacent-center pairs, both phases.')


def check_history_thresholds():
    assert [threshold_after_history([letter]) for letter in range(7)] == [5, 6, 7, 7, 7, 9, 9]
    # An independent finite stream calculation also handles an internal strip
    # failure. The shared stream engine acts on the input in chronological order.
    checks = 0
    for size in range(4):
        for history in product(range(8), repeat=size):
            threshold = threshold_after_history(history)
            for incoming in range(1 + 6 + 5 * size):
                final = incoming + 1 if incoming else 0
                stream = Stream(history + (final,), (2,))
                for _ in history:
                    stream = next_stream(stream)
                    if stream is None:
                        break
                if threshold is None:
                    assert stream is None
                else:
                    assert stream is not None and (debt_of(stream.first()) >= 6) == (incoming >= threshold)
                    checks += 1
    print(f'Fixed-column history: {checks} surviving history/debt cases checked through three updates.')





def check_survivor_runs():
    # A body closing is a 0-to-1 change in the old survivor sequence.
    words = [(OPEN, NEUTRAL) * 7 + (OPEN, CLOSE)]
    for size in range(2, 10):
        words.extend(body + (OPEN, CLOSE) for body in product(ALPHABET, repeat=size - 2))
    outcomes = set()
    for word in words:
        successor, low = word_sweep(word, TERNARY_CLOSE)
        if successor is None:
            continue
        guard = -low
        previous = VIRTUAL[guard]
        rises = maximum = 0
        for position, letter in enumerate(reversed(match_letters(word)), 1):
            current = letter == 1
            if current and not previous:
                rises += 1
                maximum = max(maximum, 3 * rises - position)
            previous = current
        threshold = 7 + balance(HEADERS[guard]) - VIRTUAL[guard]
        assert tuple(successor[-2:]) == (OPEN, CLOSE)
        following, _ = word_sweep(successor, TERNARY_CLOSE)
        assert (following is None) == (maximum >= threshold)
        outcomes.add(following is None)
    assert outcomes == {False, True}
    print('Survivor runs: spacing criterion agrees with the next sweep, including a physical failing word.')

def check_delayed_blocks():
    for k in (2, 4, 8, 16, 32, 64, 128, 256):
        delay = 2 * k - 1
        block = (CLOSE,) + (OPEN,) * (3 * k - 2)
        cells = list(normalized35(reversed(block)))
        for _ in range(delay):
            letter = 2
            for i, symbol in enumerate(cells):
                cells[i], letter = run_cell(symbol, letter)
            assert letter == 2
        critical = normalized35(reversed(cells))
        assert balance(critical) == -1
        at_one = match_letters(critical, incoming=1)
        assert at_one[-1] == 3 and 1 not in at_one  # no opening survived

    for k, steps in ((2, 791), (4, 2645)):
        delay = 2 * k - 1
        block = (CLOSE,) + (OPEN,) * (3 * k - 2)
        copies = threshold_after_history((2,) * delay) - 1
        assert copies == 7
        word = block * copies + (CLOSE,)
        genuine = [CLOSE]
        modified = TapeMachine(TERNARY_CLOSE, word, left=1)
        for offset in range(delay + 1):
            genuine, low = word_sweep(genuine, TERNARY_CLOSE)
            word, observed = word_sweep(word, TERNARY_CLOSE)
            assert direct_epoch(modified, ALPHABET) == word
            if offset < delay:
                assert word is not None and observed == low
            else:
                assert genuine is not None and word is None and observed == -6
        assert (modified.steps, modified.state, modified.tape[modified.head]) == (steps, 'B', 4)
    # Replace the terminal C of an entire genuine epoch-181 tape. Check the
    # exact two adjacent multiplicities on either side of the threshold.
    genuine = []
    for _ in range(181):
        genuine, _ = word_sweep(genuine, TERNARY_CLOSE)
    original = tuple(genuine)
    delay = 63
    expected = []
    for _ in range(delay + 1):
        expected.append(deficit(genuine))
        if len(expected) <= delay:
            genuine, _ = word_sweep(genuine, TERNARY_CLOSE)
    copies = 5 + balance(genuine[:-1])
    assert copies == 274 and expected[-1] == 0
    block = (CLOSE,) + (OPEN,) * 94
    for count in (copies - 1, copies):
        altered = original[:-1] + block * count + (CLOSE,)
        assert altered[:len(original)] == original
        width = len(altered)
        opens, closes = encode(normalized35(altered))
        for offset in range(delay + 1):
            survivors, guard, _ = match(width, opens, closes, 0)
            if offset < delay:
                assert guard == expected[offset]
                width, opens, closes = packed_successor(width, survivors, guard)
            else:
                assert guard == (5 if count < copies else 6)
    print('Delayed-debt blocks: k = 2, 4, ..., 256; literal B4 after 791 and 2645 steps on altered tapes.')
    print('Epoch-181 extension: 63 unchanged guards; on the next sweep 273 copies give 5, 274 copies give 6, blank gives 0.')


def check_physical_splice():
    word = tuple(map(int, '311123111121112111212112112'))
    fixed_index = len(word) - 1
    concrete = TapeMachine(TERNARY_CLOSE, word, left=1)
    readings = []
    for _ in range(8):
        readings.append(match_letters(word)[fixed_index])
        word, _ = word_sweep(word, TERNARY_CLOSE)
        assert direct_epoch(concrete, ALPHABET) == word
    assert readings == [0, 2, 3, 1, 1, 0, 1, 4] and word is None
    assert (concrete.steps, concrete.head, concrete.state, concrete.tape[concrete.head]) == (1169, -9, 'B', 4)
    print('Physical splice: seven matching samples; the 27-cell altered tape reaches B4 after 1169 instructions.')

def packed_successor(width, survivors, guard):
    preceding = (survivors >> 1) | (VIRTUAL[guard] << (width - 1))
    ordinary_opens = ~(preceding ^ survivors) & ((1 << width) - 1)
    ordinary_closes = ~preceding & survivors
    header_opens, header_closes = HEADER_MASKS[guard]
    return (width + 1 + len(HEADERS[guard]),
            (header_opens << (width + 1)) | (ordinary_opens << 1),
            (header_closes << (width + 1)) | (ordinary_closes << 1) | 1)


def unpack(width, opens, closes):
    return tuple(OPEN if opens & (1 << j) else CLOSE if closes & (1 << j) else NEUTRAL
                 for j in reversed(range(width)))


def check_observed_histories():
    for size in range(1, 9):
        for body in product(ALPHABET, repeat=size - 1):
            word = body + (CLOSE,)
            opens, closes = encode(normalized35(word))
            survivors, guard, _ = match(size, opens, closes, 0)
            successor, _ = word_sweep(word, TERNARY_CLOSE)
            if successor is None:
                assert guard >= 6
            else:
                assert packed_successor(size, survivors, guard) == (len(successor), *encode(normalized35(successor)))

    # An interval [first,last] of samples at each fixed right-index, including
    # the birth sample at offset 0. Only these short windows are needed.
    intervals = {181: (0, 7), 1204: (512, 516), 3118: (451, 452)}
    widths = {}
    windows = {birth: [] for birth in intervals}
    observed = set()
    largest = 0
    closest = None
    susceptible = Counter()
    last_quarter_failure = None
    least_later_margin = None
    width, opens, closes = 1, 0, 1
    for epoch in range(1, 25_001):
        survivors, guard, exterior = match(width, opens, closes, min(width, 8))
        assert guard < 6
        if epoch in intervals:
            widths[epoch] = width
        for birth, (first, last) in intervals.items():
            if first <= epoch - birth <= last:
                old_width = widths[birth]
                _, _, debt = match(width, opens, closes, width - old_width)
                survivor = (survivors >> (old_width - 1)) & 1
                windows[birth].append(debt + 1 if debt else survivor)
        if epoch == 181:
            assert unpack(8, opens >> (width - 8), closes >> (width - 8)) == tuple(map(int, '31112311'))
        if epoch == 188:
            split = widths[181]
            strip = unpack(width - split, opens >> split, closes >> split)
            assert ''.join(map(str, strip)) == '23213123231232'
            assert (balance(strip), deficit(strip)) == (-3, 3)
            assert canonical_replay(strip, 3) == (None, -6)
        if epoch >= 5:
            tail = width - 8
            prefix = (opens >> tail, closes >> tail)
            threshold = 6 + prefix[0].bit_count() - prefix[1].bit_count()
            assert exterior < threshold
            observed.add((prefix, exterior))
            largest = max(largest, exterior)
            if closest is None or threshold - exterior < closest[0]:
                closest = (threshold - exterior, epoch)
            if threshold == 5:
                susceptible[unpack(8, *prefix), exterior] += 1
        quarter = (width + 3) // 4
        if epoch >= 10 and 20 <= quarter <= width - 5:
            start_opens = opens >> (width - quarter)
            start_closes = closes >> (width - quarter)
            _, prefix_debt, _ = match(quarter, start_opens, start_closes, 0)
            last_five = deficit(unpack(5, opens & 31, closes & 31))
            prefix_balance = start_opens.bit_count() - start_closes.bit_count()
            margin = quarter + 8 * prefix_balance - (width - 27 + 8 * last_five)
            if prefix_debt >= 6 or margin < 0:
                last_quarter_failure = epoch
                least_later_margin = None
            elif least_later_margin is None or margin < least_later_margin[0]:
                least_later_margin = (margin, epoch)
        width, opens, closes = packed_successor(width, survivors, guard)

    assert (len({p for p, _ in observed}), len(observed), largest, closest) == (32, 35, 2, (3, 46))
    assert last_quarter_failure == 443 and least_later_margin == (16, 495)
    assert susceptible == {(tuple(map(int, '23213123')), 2): 281}
    assert windows == {181: [0, 2, 3, 1, 1, 0, 1, 1], 1204: [1, 1, 0, 1, 4], 3118: [1, 4]}
    genuine = windows[181]
    assert threshold_after_history(genuine[:7]) == 3
    assert genuine[3:7] == windows[1204][:-1]
    assert genuine[6:7] == windows[3118][:-1]
    assert (3118 - 181) % 89 == (452 - 7) % 89 == 0
    for donor in (1204, 3118):
        dangerous = Stream(tuple(genuine[:7] + [windows[donor][-1]]), (2,))
        for _ in range(7):
            dangerous = next_stream(dangerous)
            assert dangerous is not None
        assert dangerous.first() == 7
    print('Blank epochs 5..25000: 32 prefixes, 35 prefix/debt pairs; maximum cut-8 debt 2, least slack 3 at epoch 46.')
    print('Quarter bound: last failed test at epoch 443; smallest later margin through 25000 is 16 at epoch 495.')
    print('Splices: recipient 181+7, donors 1204+516 (four shared letters) and 3118+452 (same two residues mod 89).')

def check_blank():
    machine = TapeMachine(TERNARY_CLOSE)
    word = direct_epoch(machine, ALPHABET)
    assert word == [CLOSE] and word == word_sweep([], TERNARY_CLOSE)[0]
    stream = FIRST_STREAM
    pending = []
    # Independent word sweeps check each new column's next eight samples.
    for epoch in range(1, 521):
        letters = match_letters(word)
        if epoch <= 513:
            pending.append((len(word) - 1, stream.take(8), epoch))
        for index, predicted, birth in pending:
            assert letters[index] == predicted[epoch - birth]
        pending = [p for p in pending if epoch - p[2] < 7]
        assert stream.first() == letters[-1] and max(stream.period) <= 2
        if epoch == 5:
            assert (machine.steps, machine.head, word) == (97, -5, list(map(int, '213111112')))
            check_prefix_graph(word)
        if epoch == 513:
            print(f'Epoch 513: width {len(word)}, chronological prefix {len(stream.prefix)}, period {len(stream.period)}.')
        successor, low = word_sweep(word, TERNARY_CLOSE)
        assert successor is not None and -low == debt_of(stream.first())
        assert len(successor) == len(word) + len(birth_columns(stream.first()))
        if epoch < 32:
            assert direct_epoch(machine, ALPHABET) == successor
        stream = next_stream(stream)
        assert stream is not None
        word = successor
    print('Checked 32 literal blank epochs, 520 word updates and 513 complete eight-sample forecasts.')


def main():
    listed = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
    assert listed[34] == TERNARY_CLOSE == '1RB2LA4RA1LA3LA_0LA3RB3LB2RB---'
    check_blank()
    check_pascal_tails()
    check_history_thresholds()
    check_survivor_runs()
    check_observed_histories()
    check_physical_splice()
    check_delayed_blocks()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
