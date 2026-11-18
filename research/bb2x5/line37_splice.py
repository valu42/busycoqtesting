"""Construct a nonblank tape which shadows 15 genuine line-37 sweeps."""

from prior_sweeps import TERNARY_OPEN, TapeMachine, word_sweep


def signatures(word):
    """Cut i gets the debt in word[i:] and survivor immediately to its left."""
    result = {}
    debt = 0
    for i in range(len(word) - 1, -1, -1):
        symbol = word[i]
        survives = symbol == 2 and debt == 0
        result[i + 1] = (debt, survives)
        debt = max(0, debt + (symbol == 1) - (symbol == 2))
    return result


def main():
    original = []
    for _ in range(169):
        original, _ = word_sweep(original, TERNARY_OPEN)
        assert original is not None
    left, right, copies = 226, 249, 133
    assert len(original) == 382
    assert ''.join(map(str, original[left:right])) == '22122322222122322122222'
    altered = original[:left] + copies * original[left:right] + original[right:]
    machine = TapeMachine(TERNARY_OPEN, altered, left=1)
    for epoch in range(169, 184):
        pairs = signatures(original)
        assert pairs[left] == pairs[right]
        assert pairs[45] == signatures(altered)[45]
        original, low = word_sweep(original, TERNARY_OPEN)
        altered, alt_low = word_sweep(altered, TERNARY_OPEN)
        assert original is not None and altered is not None and alt_low == low
        header = 4 if low else 1
        left += header
        right += header
        assert altered == original[:left] + copies * original[left:right] + original[right:]

    assert (left, right) == (244, 267)
    block = original[left:right]
    assert block.count(2) - block.count(1) == -1
    assert signatures(original)[45][0] == 0
    assert signatures(altered)[45][0] == 24
    assert word_sweep(altered, TERNARY_OPEN) == (None, -2)
    assert word_sweep(original, TERNARY_OPEN)[0] is not None
    while machine.steps < 625797 and machine.step():
        pass
    assert (machine.steps, machine.head, machine.state, machine.tape[machine.head]) == (625796, -20, 'B', 4)
    print('One 23-cell strip at blank epoch 169 can be copied through 15 sweeps.')
    print('With 133 total copies, cut-45 debt jumps from 0 to 24 at epoch 184.')
    print('The altered tape halts at B4 after 625796 defined transitions.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    main()
