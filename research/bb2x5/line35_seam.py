"""Check the fixed zero-debt cuts and the 47-cell pattern seen on the blank tape."""
import argparse

from line35_band import Band, HEADERS, O, C, N, digits, epoch_five, load_checkpoint
from line35_band_control import BLOCK, convert
from line35_pressure import column
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch


def cut_signal(word, right_cells):
    return convert(word[-right_cells:])[1]


def cut_rule():
    # The source triple's rightmost O is one cell farther from the cap than the
    # completed inner triples. The previous center is C at the bare cap.
    for center in (O, C, N):
        temporary, odd = convert(bytes([O]), (0, int(center != C)))
        _, even = convert(temporary, (int(center == N), int(center == O)))
        assert odd == (0, 1) and even == (0, int(center == O))
    print('Every cut at 3i right cells inside i covered triples has zero debt on both sweeps.')


def control_period(path):
    record, band = load_checkpoint(path)
    k = band.count
    if not k:
        raise ValueError('at least one covered triple is required')
    # The right edge of the active strip sees survivor 1 on the odd sweep,
    # then 1-H_{k-1} on the even sweep. The incoming matching debt is always zero.
    index = k - 1
    period = 1 << index.bit_length()
    h = column(1 | (band.nonopen << 1), index, period)
    assert period == 1 or h[:period // 2] != h[period // 2:]
    print('epoch', record['epoch'], 'zero-debt right cells', 3 * k,
          'remaining left cells', band.length - 3 * k, 'paired control period', period,
          'even survivor ones', period - sum(h))


def circular_rows():
    # Store physical digits in order of increasing distance from the right.
    row = BLOCK[::-1]
    rows = [row]
    signals = []
    while row.count(O) > row.count(C):
        w = row[::-1]
        _, seed = convert(w)
        _, fixed = convert(w, seed)
        new, end = convert(w, fixed)
        assert end == fixed
        outgoing = []
        signal = fixed
        for symbol in row:
            _, signal = convert(bytes([symbol]), signal)
            outgoing.append(signal)
        signals.append(outgoing)
        row = new[::-1]
        rows.append(row)
    assert len(rows) == 889 and rows[-1].count(C) - rows[-1].count(O) == 1
    return rows, signals


def interval(row, start, length=47):
    return bytes(row[(start + j) % 47] for j in range(length))


def births():
    packets = []
    for guard, header in enumerate(HEADERS):
        for left in ((0, 1) if guard == 0 else (0,)):
            virtual = int(guard < 2)
            first = O if virtual == left else C if left else N
            packets.append(bytes([first]) + bytes(map(int, header[::-1])))
    return packets


def birth_bound(rows):
    # State j means the previous outermost column has ring phase j. The value
    # is the greatest trailing match of newborn digits, across arbitrary packets.
    lengths = [0] * 47
    maximum = 0
    packets = births()
    for row in rows[1:]:
        following = [0] * 47
        for j, matched in enumerate(lengths):
            for packet in packets:
                suffix = matched
                for offset, symbol in enumerate(packet, 1):
                    suffix = suffix + 1 if symbol == row[(j + offset) % 47] else 0
                    maximum = max(maximum, suffix)
                end = (j + len(packet)) % 47
                following[end] = max(following[end], suffix)
        lengths = following
    assert maximum == 45
    print('Maximum consecutive matching newborn digits along the 888 updates:', maximum)


def blank_hit(rows, signals, words):
    band, _, _ = epoch_five()
    # Fixed indices 1350 through 1396, counted outward from the right.
    start = 1350
    for epoch in range(5, 1083, 2):
        if epoch <= 979:
            assert (band.count >= 450) == (epoch == 979)
        for offset, signal in enumerate(band.signals()):
            now = epoch + offset
            if 1069 <= now <= 1082:
                word = words[now]
                assert band.length == len(word)
                assert digits(band.width, band.opens, band.closes) == word[:band.width]
                if not offset:
                    assert band.unpack() == word
                phase = now - 194
                actual = word[::-1][start:start + 47]
                expected = interval(rows[phase], 2)
                if now <= 1074:
                    assert actual == expected
                if now == 1074:
                    assert cut_signal(word, start) == (0, 1)
                    assert signals[phase][1] == (1, 0)
                if now == 1075:
                    assert sum(a != b for a, b in zip(actual, expected)) == 3
                if now == 1082:
                    assert actual.count(O) - actual.count(C) == 11
                    assert expected.count(O) - expected.count(C) == -1
            cost, guard = band.half(*signal)
            assert cost is not None
        band.advance_centers()
    print('Blank epochs 1069 through 1074 match 47 cells. At 1074 the real cut sends (0,1), the circular cut (1,0).')


def uncovered_hit(rows, words):
    # The same final, negatively balanced row also occurs beyond the protected region.
    start = 3213
    for epoch, phase in ((2021, 887), (2022, 888)):
        word = words[epoch]
        assert word[::-1][start:start + 47] == interval(rows[phase], 25)
    word = words[2022]
    assert len(word) == 4112 and Band.from_word(words[2021]).count * 3 == 2451
    assert (len(word) - start - 47, len(word) - start) == (852, 899)
    assert cut_signal(word, start) == (0, 1)
    assert cut_signal(word, start + 47) == (1, 0)
    assert word[::-1][start + 47:start + 49] == bytes([N, O])
    assert cut_signal(word, start + 48)[0] == 1
    assert cut_signal(word, start + 49)[0] == 0
    assert cut_signal(word, len(word)) == (0, 1)
    print('Blank epoch 2022 contains the negative circular row outside the protected suffix.')
    print('It sends one unit of debt left. The next neutral passes it, the following opener absorbs it.')


def finite_seed(rows):
    start, phase = 107, 44
    word = interval(rows[start], phase + 1, 94)[::-1] + bytes([O, C])
    machine = TapeMachine(TERNARY_CLOSE, word, left=1)
    initial = len(word)
    newborn = differences = 0
    for t in range(start + 1, start + 50):
        old = len(word)
        word = bytes(direct_epoch(machine, (O, C, N)))
        added = len(word) - old
        expected = interval(rows[t], phase + newborn + 1, added)
        for i, (a, b) in enumerate(zip(word[:added][::-1], expected)):
            if newborn + i < 47:
                differences += int(a != b)
        newborn += added
        actual = word[::-1][initial:initial + 47]
        assert (actual == interval(rows[t], phase + 1)) == (t == 156)
    assert differences == 24 and machine.steps == 24195
    print('The 96-cell nonblank seed corrects 24 birth mismatches and matches a complete copy after 49 sweeps.')


def observed_words(literal):
    # Use the repository's ordinary word interpreter to check event locations from blank.
    from prior_sweeps import word_sweep
    observed = {}
    word = []
    machine = TapeMachine(TERNARY_CLOSE) if literal else None
    for t in range(1, 2023):
        word, _ = word_sweep(word, TERNARY_CLOSE)
        if machine is not None:
            assert direct_epoch(machine, (O, C, N)) == word
        if 1069 <= t <= 1082 or t in (2021, 2022):
            observed[t] = bytes(word)
    if machine is not None:
        print('Literal blank epoch 2022 at raw step', machine.steps, 'head', machine.head)
    return observed


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--literal', action='store_true', help='also replay blank to epoch 2022 instruction by instruction')
    parser.add_argument('--checkpoint', help='compute the complete control period of its outermost zero-debt cut')
    args = parser.parse_args()
    cut_rule()
    orbit, letters = circular_rows()
    birth_bound(orbit)
    observed = observed_words(args.literal)
    blank_hit(orbit, letters, observed)
    uncovered_hit(orbit, observed)
    finite_seed(orbit)
    if args.checkpoint:
        control_period(args.checkpoint)
