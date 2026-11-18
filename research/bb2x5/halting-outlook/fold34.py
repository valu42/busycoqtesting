"""Check folded matching coordinates and adjacent-sweep transport on line 34."""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from prior_sweeps import TERNARY, TapeMachine, word_sweep
from target34_orbit import analyze, encode


def match(word):
    """At cut i, give debt in word[i:]. Opening survival is attached to cells."""
    size = len(word)
    debt = [0] * (size + 1)
    survivor = [0] * size
    for i in reversed(range(size)):
        survivor[i] = int(word[i] == 1 and debt[i + 1] == 0)
        debt[i] = max(0, debt[i + 1] + (word[i] == 3) - (word[i] == 1))
    return debt, survivor


def starts(bits, virtual):
    return [i for i, bit in enumerate(bits) if bit and not (bits[i - 1] if i else virtual)]


def score(cut, rising, previous):
    return max([0] + [3 * n + previous - 2 - (p - cut)
                      for n, p in enumerate((p for p in rising if p >= cut), start=1)])


def check_word(word, direct=True):
    debt, bits = match(word)
    result, low = word_sweep(word, TERNARY)
    assert -low == min(6, debt[0])
    if result is None:
        return
    h = 1 if debt[0] < 3 else 5
    virtual = int(debt[0] == 1)
    debt2, bits2 = match(result)
    rising = starts(bits, virtual)
    ordinary_bits = [virtual] + bits
    # The monotone folded coordinate is defined on cuts of the successor's ordinary data.
    folded = [j + ordinary_bits[j] - debt2[h + j] for j in range(len(word) + 1)]
    for j in range(len(word)):
        assert folded[j + 1] - folded[j] == 3 * (result[h + j] == 3) + bits2[h + j]
    for a in range(len(word) + 1):
        assert score(a, rising, ordinary_bits[a]) == debt2[h + a]
        if a and debt[a]:
            assert bits[a - 1] == 0
            b = next((i for i in range(a, len(word)) if bits[i]), len(word))
            assert result[h + a:h + b] == [1] * (b - a)
            assert debt2[h + a] == max(0, debt2[h + b] - (b - a))
            end_open = a
            while end_open < len(word) and word[end_open] == 1:
                end_open += 1
            old_length = end_open - a
            assert end_open < len(word) and debt[end_open] == old_length + debt[a]
            assert b - a >= 2 * old_length + debt[a]
    for a, b in zip(rising, rising[1:]):
        assert debt2[h + a] == 1 + max(0, debt2[h + b] + 2 - (b - a))
    if direct:
        accelerated, guard, _, _ = analyze(encode(word), ())
        target, header, clock = accelerated
        assert header == h and target == encode(result)
        machine = TapeMachine(TERNARY, word, left=1)
        for _ in range(clock):
            assert machine.step()
        assert machine.state == 'A' and machine.head == -h and machine.steps == clock
        assert machine.tape == {machine.head + 1 + i: v for i, v in enumerate(result)}


def check_generation(word):
    old_debt, old_survival = match(word)
    new, _ = word_sweep(word, TERNARY)
    if new is None:
        return
    old_h = 1 if old_debt[0] < 3 else 5
    h_debt, survival = match(new)
    if h_debt[0] >= 6:
        return
    virtual = int(h_debt[0] == 1)
    rising = starts(survival, virtual)
    for a, b in zip(rising, rising[1:]):
        if a < old_h:
            continue
        stop = a
        while survival[stop]:
            stop += 1
        z = b - stop
        left = old_survival[stop - 1 - old_h] if stop > old_h else int(old_debt[0] == 1)
        right = old_survival[b - 1 - old_h] if b > old_h else int(old_debt[0] == 1)
        assert z == 3 * new[stop:b].count(3) + left - right
        if b - a == 2:
            assert new[a:b + 1] == [1, 2, 1] and left == 1 and right == 0


def audit():
    assert (HERE.parent / 'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[33] == TERNARY
    count = 0
    for width in range(9):
        for word in product((1, 2, 3), repeat=width):
            check_word(word)
            check_generation(word)
            count += 1
    print(f'Exhaustive inputs through length 8: {count}; all successful first sweeps checked literally.')


def dense_starts(config):
    """Output all run starts in material order via the exact matching slots."""
    import numpy as np

    width, opens, closes = config
    guard = occupied_cuts = 0
    while closes:
        slot = ((closes + ~opens) ^ closes ^ ~opens)
        guard += (slot >> width) & 1
        occupied_cuts |= slot
        closes &= slot
        opens &= ~slot
    assert guard < 6 and width
    prev = (opens >> 1) | (int(guard == 1) << (width - 1))
    rises = opens & ~prev
    count = (width + 7) // 8
    padded = np.frombuffer(rises.to_bytes(count, 'big'), dtype=np.uint8)
    indices = np.flatnonzero(np.unpackbits(padded)) - (8 * count - width)
    return indices, opens, occupied_cuts & ((1 << (width + 1)) - 1)


def genuine_six(config, successor, header):
    def word_of(value):
        width, openings, closings = value
        a = format(openings, f'0{width}b')
        b = format(closings, f'0{width}b')
        return [1 if o == '1' else 3 if c == '1' else 2 for o, c in zip(a, b)]
    old, new = word_of(config), word_of(successor)
    debt, survive = match(old)
    debt2, _ = match(new)
    cut = debt.index(max(debt))
    b = next(i for i in range(cut, len(old)) if survive[i])
    assert (cut, debt[cut], b-cut, debt2[cut+header], debt2[b+header]) == (12645, 6, 38, 0, 1)
    assert new[cut+header:b+header] == [1] * 38
    print('Blank epoch 14117: cut 12645 with debt 6 becomes 38 openings; '
          'new debt at material cut 0, at their far end 1.')


def corridor_controls():
    # Explicit finite, nonblank tapes. The material cut is inside the variable word.
    short = '111222222212221222222122212222221222122222'
    four = '1113121122211222112221' + '12222' * 22 + '112'
    examples = [(32, short, 6, 7), (40, four, 3, 4)]
    for pad, seed, offset, last_epoch in examples:
        word = [1] * pad + list(map(int, seed)) + [1] * 12
        a = pad + offset
        machine = TapeMachine(TERNARY, word, left=1)
        observations = []
        for t in range(last_epoch + 1):
            debt, _ = match(word)
            length = 0
            while a + length < len(word) and word[a + length] == 1:
                length += 1
            observations.append((debt[a], length))
            if t == last_epoch:
                break
            new, _ = word_sweep(word, TERNARY)
            result, _, _, _ = analyze(encode(word), ())
            target, header, ticks = result
            old_head = machine.head
            for _ in range(ticks):
                assert machine.step()
            assert target == encode(new)
            assert (machine.state, machine.head) == ('A', old_head-header)
            assert machine.tape == {machine.head + 1 + i: v for i, v in enumerate(new)}
            word, a = new, a + header
        expected = ([(0, 0), (0, 4), (0, 3), (0, 3), (1, 0), (1, 1), (1, 4), (0, 34)]
                    if seed == short else [(1, 0), (1, 1), (1, 4), (1, 22), (0, 130)])
        assert observations == expected
        print(f'Nonblank interior length {len(seed)}, through literal step {machine.steps}:',
              observations)


def splice_control():
    word = []
    for _ in range(839):
        word, _ = word_sweep(word, TERNARY)
    altered = word[:856] + 493 * word[856:879] + word[879:]
    for _ in range(839, 853):
        word, _ = word_sweep(word, TERNARY)
        altered, _ = word_sweep(altered, TERNARY)
    for label, source in (('blank', word), ('altered', altered)):
        debt, survivor = match(source)
        new, _ = word_sweep(source, TERNARY)
        assert new is not None
        h = 5 if debt[0] >= 3 else 1
        a = 12 - h
        threshold = 6 + new[:12].count(1) - new[:12].count(3)
        rising = [j for j in starts(survivor, int(debt[0] == 1)) if j >= a]
        scored = [(3*n + survivor[a-1] - 2 - (j-a), n, j)
                  for n, j in enumerate(rising, start=1)]
        first = next((row for row in scored if row[0] >= threshold), None)
        assert threshold == 12 and max(scored[:64])[0] == 1
        assert max(scored)[0] == match(new)[0][12]
        if label == 'altered':
            assert first == (12, 4065, 12192)
            assert word_sweep(new, TERNARY) == (None, -6)
        else:
            assert first is None and max(scored)[0] == 1
        print(f'Input epoch 853, {label}: threshold {threshold}, '
              f'first crossing (score, rank, material position) {first}, '
              f'first-64 peak {max(scored[:64])[0]}, overall peak {max(scored)[0]}.')


def orbit(epochs):
    import numpy as np

    cfg = (0, 0, 0)
    headers = (9, 12)
    clock = 0
    debt_pairs = Counter()
    witnesses = {}
    bands = [(1, 4), (5, 8), (9, 16), (17, 32), (33, 64), (65, None)]
    least = {}
    held_out = {}
    streaks = []
    streak_records = []
    previous_append = 0
    for t in range(epochs):
        transition, guard, old_ds, _ = analyze(cfg, (7, 11))
        successor, h, cost = transition
        if t == 14117:
            genuine_six(cfg, successor, h)
        if cfg[0] >= 16:
            a = 12 - h
            debt_old = old_ds[0 if a == 7 else 1]
            x, survivor, occupied = dense_starts(cfg)
            # Old material cuts gain one bit of right-distance when the old right edge appended.
            here = occupied & ((1 << (cfg[0] - 10)) - 1)  # cut index >= 11
            longer = [(mask << previous_append) & here for mask in streaks]
            streaks = ([here] if here else []) + [mask for mask in longer if mask]
            if len(streaks) > len(streak_records):
                cut = cfg[0] + 1 - streaks[-1].bit_length()
                streak_records.append((len(streaks), t, cut))
            x = x[np.searchsorted(x, a):]
            previous = (survivor >> (cfg[0] - a)) & 1
            n = np.arange(1, len(x) + 1)
            estimated = 3 * n + previous - 2 - (x - a)
            expr = max(0, int(estimated.max())) if len(x) else 0
            out_transition, _, out_ds, _ = analyze(successor, headers)
            assert out_transition is not None and out_ds[1] == expr
            debt_pairs[debt_old, expr] += 1
            if debt_old and expr and (debt_old, expr) not in witnesses:
                witnesses[debt_old, expr] = (t, a)
            # The remaining raw threshold has to pay the balance of the next physical prefix.
            width, op, cl = successor
            balance = (op >> (width - 12)).bit_count() - (cl >> (width - 12)).bit_count()
            margins = 6 + balance - estimated
            for lo, hi in bands:
                segment = margins[lo - 1:hi]
                if len(segment):
                    i = int(segment.argmin()) + lo - 1
                    item = (int(margins[i]), t, i + 1, int(x[i]))
                    band = lo, hi
                    if band not in least or item < least[band]:
                        least[band] = item
                    if t >= 12000 and (band not in held_out or item < held_out[band]):
                        held_out[band] = item
        previous_append = successor[0] - cfg[0] - h
        cfg = successor
        clock += cost
    print(f'Blank run: {epochs} completed sweeps, raw clock {clock}, width {cfg[0]}.')
    print('First streak of each length at material cuts with index >= 11 (length, last epoch, last cut):',
          streak_records)
    print('Ordered pair counts (old material debt, new cut-12 debt):', sorted(debt_pairs.items()))
    print('First consecutive-positive records (input epoch, old cut):', sorted(witnesses.items()))
    print('Run-rank band, minimum signed margin to B4, input epoch, rank, old run-start position:')
    for band in bands:
        print(band, least.get(band))
    if held_out:
        print('Same margins on held-out input epochs 12000 onward:')
        for band in bands:
            print(band, held_out.get(band))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, default=4096)
    args = parser.parse_args()
    if not __debug__ or args.epochs < 14:
        parser.error('enable assertions and use at least 14 epochs')
    audit()
    splice_control()
    corridor_controls()
    orbit(args.epochs)
