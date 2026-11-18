"""Check the line-37 right-suffix theorem against the word and literal TM rules."""

from itertools import product
from pathlib import Path

from prior_sweeps import TERNARY_OPEN, TapeMachine, direct_epoch, word_sweep


def digit(left_bit, right_bit):
    if left_bit == right_bit:
        return 2
    return 1 if right_bit else 3


def column_pass(cells, right_bit, debt):
    """cells are listed from right to left, immediately beyond a known suffix."""
    result = []
    for symbol in cells:
        survives = symbol == 2 and debt == 0
        result.append(digit(survives, right_bit))
        debt = max(0, debt + (symbol == 1) - (symbol == 2))
        right_bit = survives
    return tuple(result)


def next_suffix(suffix):
    # A final 2 is always an unmatched opening. It yields the appended 2.
    assert suffix and suffix[0] == 2
    return (2,) + column_pass(suffix[1:], True, 0)


def outer_triplet(triple, center):
    intermediate = column_pass(triple, center != 1, 0)
    return column_pass(intermediate, center == 2, int(center == 3))


def clean_centers(word):
    suffix = word[::-1]
    centers = []
    for j in range(0, len(suffix) - 2, 3):
        first, center, third = suffix[j:j + 3]
        if first != 2 or third != 2:
            break
        centers.append(center)
    return centers


def advance_centers(centers):
    right_bit = True
    result = []
    for center in centers:
        is_open = center == 2
        result.append(digit(is_open, right_bit))
        right_bit = is_open
    return result


def main():
    assert Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[36] == TERNARY_OPEN
    alphabet = (1, 2, 3)
    triples = tuple(product(alphabet, repeat=3))
    clean = {(2, x, 2) for x in alphabet}
    for center, previous in product(alphabet, repeat=2):
        assert outer_triplet((2, center, 2), previous) == (2, digit(center == 2, previous == 2), 2)
    for previous, triple in product(alphabet, triples):
        assert outer_triplet(outer_triplet(triple, 3), previous) in clean

    # Test the boundary across arbitrary successful inputs, including guard resets.
    audit = [0, 0]
    for length in range(1, 8):
        for body in product(alphabet, repeat=length - 1):
            word = body + (2,)
            successor, low = word_sweep(word, TERNARY_OPEN)
            if successor is not None:
                assert next_suffix(word[::-1]) == tuple(successor[::-1][:length])
                audit[-low] += 1

    machine = TapeMachine(TERNARY_OPEN)
    word = []
    old_centers = []
    for epoch in range(1, 1002):
        word, _ = word_sweep(word, TERNARY_OPEN)
        assert word is not None
        if epoch <= 32:
            assert word == direct_epoch(machine, alphabet)
        if epoch == 7:
            assert machine.steps == 151 and word == list(map(int, '2221313222212'))
        if epoch % 2:
            centers = clean_centers(word)
            assert centers[:len(old_centers)] == advance_centers(old_centers)
            old_centers = centers
    assert len(word) == 2271 and len(old_centers) == 372
    print(f'Suffix rule: {audit[0]} no-reset and {audit[1]} reset inputs checked.')
    print('All 9 clean transitions and 81 two-input synchronization cases checked.')
    print('Blank epoch 7: two clean right triples at step 151.')
    print('Blank epoch 1001: 372 clean triples in a word of 2271 cells.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    main()
