"""Check failure of the two-sweep implication on a history with known ordinary ancestry."""
from line35_band import Band, O, C, N, HEADERS, mask_of
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


def cut_signal(band, cells):
    """Debt and survivor just to the left of this many right-indexed cells."""
    j = cells - 2  # The bare terminal cap sends (0, 0).
    mask = (1 << j) - 1
    o, c = band.opens & mask, band.closes & mask
    debt = 0
    while c:
        busy = (c + ~o) ^ c ^ ~o
        debt += (busy >> j) & 1
        o &= ~busy
        c &= busy
    return debt, (o >> (j - 1)) & 1


def convert(word, signal=(0, 0)):
    """One pass in fixed right-index coordinates, with an explicit input signal."""
    debt, right = signal
    out = bytearray()
    for symbol in reversed(word):
        current = int(symbol == O and not debt)
        out.append(O if current == right else C if right else N)
        debt = max(0, debt + (symbol == C) - (symbol == O))
        right = current
    return bytes(reversed(out)), (debt, right)


def balance(word):
    return word.count(O) - word.count(C)


def check_margin_change(epoch, word, cut):
    band = Band.from_word(word)
    m = band.width
    x = (m + 4) // 5
    left = word[:-cut - 47]
    block = word[-cut - 47:-cut]
    tail = word[len(left):x]
    assert 0 <= x - len(left) <= 47 and cut >= band.length - m + 3
    assert balance(left) > 47 + len(tail)
    if epoch == 657:
        assert balance(block) == 23 and band.paired_test(5)[1] == -15
        return
    assert epoch == 655 and balance(block) == 35
    # Zero-debt matching of the test prefix itself must also repeat through the block.
    tail_out, signal = convert(tail)
    block_out, emitted = convert(block, signal)
    assert emitted == signal and balance(block_out) == 32
    left_out, (guard, bit) = convert(left, signal)
    assert guard == 0
    header = bytes(map(int, HEADERS[guard]))
    virtual = int(guard < 2)
    new_left = header + bytes([O if bit == virtual else C if bit else N]) + left_out
    y = (m + len(header) + 1 + 4) // 5
    assert len(new_left) <= y <= len(new_left) + len(tail_out)
    assert balance(new_left) > 47 + len(tail_out)
    assert band.paired_test(5) == (0, 2982, 1, 2175)


def unbounded_reserves():
    # The same marked 47 right indices appear at every sample.
    cut = 52163
    word = planted_odd_word()
    band = Band(len(word) - 2, mask_of(word[:-2], O), mask_of(word[:-2], C))
    for epoch in range(401, 1289):
        inside, outside = cut_signal(band, cut), cut_signal(band, cut + 47)
        if epoch < 1288:
            assert inside == outside
        if epoch in (655, 657):
            check_margin_change(epoch, band.unpack(), cut)
        if epoch == 1288:
            word = band.unpack()
            block = word[-cut - 47:-cut]
            assert balance(block) == -1
            assert inside == (1074, 0) and outside == (1075, 0)
            assert inside[0] > len(block)
        cost, guard = band.half(0, 0, 1)
        assert (cost is None) == (epoch == 1288)
    print('Repeatable 47-cell block: adding ten copies changes margins by +23,+17 at 655 and -1 at 657.')


def main():
    unbounded_reserves()
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
