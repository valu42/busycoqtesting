"""Check failure of the two-sweep implication on a history with known ordinary ancestry."""
from line35_band import Band, O, C
from prior_sweeps import TERNARY_CLOSE, word_sweep

BLOCK = bytes(map(int, '12323112321132311123213121323112111311211311213'))


def planted_odd_word():
    word = []
    for _ in range(400):
        word, _ = word_sweep(word, TERNARY_CLOSE)
    word = tuple(word) + tuple(BLOCK) * 1358 + (C,)
    word, _ = word_sweep(word, TERNARY_CLOSE)
    return bytes(word)


def row(epoch, band):
    return epoch, band.width, band.paired_test(5)


def replay(padding):
    word = planted_odd_word()
    if padding:
        # In physical order the outermost triple is O,C,O and the others are all O.
        word = word[:-2] + bytes([O, C, O]) + bytes([O]) * (3 * (padding - 1)) + word[-2:]
    band = Band.from_word(word)
    chosen = {}
    for epoch in range(401, 1289, 2):
        if epoch in (655, 657, 1283, 1285):
            chosen[epoch] = row(epoch, band)
        for offset, signal in enumerate(band.signals()):
            cost, guard = band.half(*signal)
            if cost is None:
                assert (epoch + offset, guard) == (1288, 6)
                return chosen
        band.advance_centers()
    raise AssertionError('missing altered-tape halt')


def main():
    cases = replay(0)
    assert cases[655][2] == (0, 2982, 1, 2175)
    assert cases[657][2] == (0, -15, 1, 1442)
    assert cases[1283][2] == (1, 2760, 0, 8)
    assert cases[1285][2] == (1, 2777, 0, -39)
    assert replay(1024) == cases
    for epoch, width, margins in cases.values():
        print('altered epoch', epoch, 'uncovered', width, 'paired test', margins)
    print('Both altered tapes reach B4 at epoch 1288.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
