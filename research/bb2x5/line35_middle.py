"""Verify a five-sweep bound on the excess of closings in the line 35 interior."""
import argparse
from functools import cache
from itertools import product

from line35_timed import encode, sweep, unpack
from prior_sweeps import TERNARY_CLOSE, word_sweep

OPEN, CLOSE, NEUTRAL = range(3)
MISSING = -1
# Left-to-right physical tape symbols. Depth counts ordinary sweep images.
FORBIDDEN = {
    "231232312323123231232312": 5,
    "231232312323121323123231232312": 5,
    "3213123231232312": 4,
}


def derivative(bits):
    return ''.join('1' if a == b else '2' if b else '3' for a, b in zip(bits, bits[1:]))


def decode(word):
    """Include the exterior bit immediately before the first ordinary cell."""
    for previous in (0, 1):
        bits = [previous]
        for symbol in word:
            if (symbol == '2' and bits[-1]) or (symbol == '3' and not bits[-1]):
                break
            bits.append(bits[-1] if symbol == '1' else int(symbol == '2'))
        else:
            yield bits


def predecessors(word):
    """Possible older ordinary words which themselves have an ordinary parent."""
    width = len(word)
    for bits in decode(word):
        survivors = bits[1:]
        first = next((i for i, bit in enumerate(survivors) if bit), width)
        # A survivor immediately left of the interval forces zero incoming debt
        # at the left cut. At an internal survivor, left debt has fallen to zero.
        maximum = first if first < width else 2 * width
        if bits[0]:
            maximum = 0

        def extend(index, left_debt, prefix, last_nonopening):
            if index == width:
                if left_debt <= width:
                    yield prefix
                return
            if survivors[index]:
                if left_debt == 0:
                    yield from extend(index + 1, 0, prefix + '1', last_nonopening)
                return
            # Run matching backwards, from the debt left of the cell to its right.
            if left_debt and last_nonopening != '2':
                yield from extend(index + 1, left_debt - 1, prefix + '2', '2')
            if last_nonopening != '3':
                yield from extend(index + 1, left_debt, prefix + '3', '3')
            yield from extend(index + 1, left_debt + 1, prefix + '1', last_nonopening)

        for start_debt in range(maximum + 1):
            yield from extend(0, start_debt, '', '')


@cache
def has_free_history(word, depth):
    if depth == 1:
        return next(decode(word), None) is not None
    return any(has_free_history(parent, depth - 1) for parent in predecessors(word))


# Relations below store a set of destinations for each possible input state.
def compose(left, right):
    return tuple(frozenset(j for i in choices for j in right[i]) for choices in left)


def balanced_classes(graph, begin, period):
    """Check the lengths of balanced paths, including their infinite periodic tail."""
    size = len(graph)
    opening, closing, neutral = [
        tuple(frozenset() if row[a] == MISSING else frozenset([row[a]]) for row in graph)
        for a in (OPEN, CLOSE, NEUTRAL)
    ]
    balanced = [tuple(frozenset([i]) for i in range(size))]
    wrapped = []
    for length in range(1, 2 * begin + 3 * period + 3):
        wrapped.append(compose(compose(opening, balanced[-1]), closing))
        result = list(compose(neutral, balanced[-1]))
        for inner in range(length - 1):
            term = compose(wrapped[inner], balanced[length - 2 - inner])
            result = [a | b for a, b in zip(result, term)]
        balanced.append(tuple(result))
    assert balanced[begin:-period] == balanced[begin + period:]
    # Length-zero and positive gaps have different emitted symbols. begin >= 1.
    assert begin >= 1
    return [compose(matrix, opening) for matrix in balanced[:begin + period]]


def minimize(rows):
    """Moore refinement. Every live state accepts an interval end."""
    partition = [0] * len(rows)
    while True:
        classes = {}
        next_partition = []
        for row in rows:
            key = tuple(MISSING if j == MISSING else partition[j] for j in row)
            next_partition.append(classes.setdefault(key, len(classes)))
        if next_partition == partition:
            return list(classes)
        partition = next_partition


def determinize(graph):
    initial = frozenset(range(len(graph)))
    states, ids, rows = [initial], {initial: 0}, []
    for choices in states:
        row = []
        for letter in (OPEN, CLOSE, NEUTRAL):
            dest = frozenset(j for i in choices for j in graph[i][letter])
            if not dest:
                row.append(MISSING)
                continue
            if dest not in ids:
                ids[dest] = len(states)
                states.append(dest)
            row.append(ids[dest])
        rows.append(tuple(row))
    return minimize(rows)


def ordinary_image(graph, begin, period):
    """Enclose every one-sweep image of a finite path, including both free edges."""
    after_gap = balanced_classes(graph, begin, period)
    width = begin + period
    result = []
    for i in range(len(graph)):
        for count in range(width):
            row = [set(), set(), set()]
            next_count = count + 1 if count + 1 < width else begin
            zero_symbol = NEUTRAL if count == 0 else OPEN
            one_symbol = OPEN if count == 0 else CLOSE
            row[zero_symbol].add(i * width + next_count)
            row[one_symbol].update(j * width for j in after_gap[count][i])
            result.append(row)
    # The first survivor may follow a partial gap with no left endpoint in the
    # window. The preceding survivor bit may initially be either zero or one.
    first = {j * width for choices in after_gap[0] for j in choices}
    no_survivor = len(result)
    result.append([{no_survivor}, first, set()])
    result.append([first, set(), {no_survivor}])
    return determinize(result)


def remove_forbidden(graph):
    prefixes = {w[:i] for w in FORBIDDEN for i in range(len(w))}
    states, ids, rows = [(0, '')], {(0, ''): 0}, []
    for state, prefix in states:
        row = []
        for symbol, dest in enumerate(graph[state], 1):
            word = prefix + str(symbol)
            if dest == MISSING or any(word.endswith(w) for w in FORBIDDEN):
                row.append(MISSING)
                continue
            while word not in prefixes:
                word = word[1:]
            key = dest, word
            if key not in ids:
                ids[key] = len(states)
                states.append(key)
            row.append(ids[key])
        rows.append(tuple(row))
    return minimize(rows)


def certify_paths(graph):
    """Integer potential for length plus eight times the opening balance."""
    costs = (9, -7, 1)
    edges = [(i, j, c) for i, row in enumerate(graph)
             for j, c in zip(row, costs) if j != MISSING]
    distance = [None] * len(graph)
    distance[0] = 0
    for _ in range(len(graph)):
        changed = False
        for i, j, cost in edges:
            if distance[i] is None:
                continue
            proposed = distance[i] + cost
            if distance[j] is None or proposed < distance[j]:
                distance[j] = proposed
                changed = True
        if not changed:
            break
    assert all(d is not None for d in distance)
    assert distance[0] == 0 and min(distance) == -25
    assert all(distance[j] <= distance[i] + cost for i, j, cost in edges)
    return min(distance)


def verify_envelope():
    graph = [(0, 0, 0)]  # all physical words
    sizes = []
    for begin, period in [(1, 1), (1, 3), (13, 3)]:
        graph = ordinary_image(graph, begin, period)
        sizes.append(len(graph))
    for word, depth in FORBIDDEN.items():
        assert not has_free_history(word, depth)
    graph = remove_forbidden(graph)
    assert sizes == [3, 12, 49] and len(graph) == 177
    print('ordinary-image state counts', sizes, 'filtered states', len(graph),
          'least potential', certify_paths(graph))
    return graph


def verify_small_windows(graph):
    for width in range(1, 7):
        for prefix in product('123', repeat=width):
            word = ''.join(prefix)
            if has_free_history(word, 5):
                state = 0
                for digit in word:
                    state = graph[state][int(digit) - 1]
                    assert state != MISSING
    assert not has_free_history('321132', 2)
    assert '321132' in '12323112321132311123213121323112111311211311213'
    print('finite-window comparisons passed')


def prefix_debt(width, opens, closes):
    debt = 0
    while closes:
        occupied = (closes + ~opens) ^ closes ^ ~opens
        debt += (occupied >> width) & 1
        opens &= ~occupied
        closes &= occupied
    return debt


def verify_blank(last_epoch):
    word = []
    for _ in range(5):
        word, _ = word_sweep(word, TERNARY_CLOSE)
    state = encode(word)
    last_miss = None
    min_margin = None
    largest_debt = 0
    for epoch in range(5, last_epoch + 1):
        n, opens, closes = state
        x = (n + 3) // 4
        if 20 <= x <= n - 5:
            mask = (1 << (x - 8)) - 1
            left_o = (opens >> (n - x)) & mask
            left_c = (closes >> (n - x)) & mask
            balance = left_o.bit_count() - left_c.bit_count()
            debt = prefix_debt(x - 8, left_o, left_c)
            largest_debt = max(largest_debt, debt)
            remainder_bound = (n - 5 - x + 25) // 8 + 1
            margin = balance + 4 - remainder_bound
            if debt > 4 or margin < 0:
                last_miss, min_margin = epoch, None
            elif min_margin is None or margin < min_margin[0]:
                min_margin = margin, epoch
        if epoch == 1406:
            assert unpack(*state)[571:589] == bytes(map(int, '232312323123231232'))
        if epoch < last_epoch:
            state, _, _, _, cut8 = sweep(*state)
            assert state is not None
            if epoch <= 523:
                assert cut8 <= 4
    print('through epoch', last_epoch, 'last quarter-test miss', last_miss,
          'smallest later margin and epoch', min_margin, 'largest prefix debt', largest_debt)
    if last_epoch == 150000:
        assert last_miss == 523 and min_margin == (19, 573) and largest_debt == 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, help='also replay the blank-orbit quarter test')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    graph = verify_envelope()
    verify_small_windows(graph)
    if args.epochs is not None:
        if args.epochs < 5:
            parser.error('the timed blank seed is at epoch five')
        verify_blank(args.epochs)
