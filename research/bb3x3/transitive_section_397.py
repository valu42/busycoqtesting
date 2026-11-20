#!/usr/bin/env python3
"""Verify the finite certificate in TRANSITIVE_SECTION_397.md."""
from check_bb33 import H397, sweep


def propagate(bits, mode):
    """Apply one carry to occupied bits, retaining any outgoing edge event."""
    for i, bit in enumerate(bits):
        bits[i], mode = H397.rules[mode][bit]
        if mode == -1:
            break
    return mode


def next_activity(activity):
    """Sum the two child-section activities of each carry modulo two."""
    return tuple(
        sum(activity[mode] for _, mode in row if mode != -1) % 2
        for row in H397.rules
    )


def main():
    word = H397.seed
    for t in range(64):
        word = sweep(H397, word, H397.modes[t % 4])
        assert word is not None
    assert ''.join(map(str, word)) == '11100010001000111011111111001'

    bits = list(word)
    section = []
    for t in range(1024):
        carry = propagate(bits, H397.modes[t % 4])
        if carry != -1:
            section.append(carry)
        if (t + 1) % 4 == 0:
            assert (tuple(bits) == word) == (t == 1023)
    section_word = ''.join('abcdef'[mode] for mode in section)
    assert section_word == 'bcbcbebcbcbcecbcbcbcffdfffffaffbc'
    assert [section.count(mode) for mode in range(6)] == [1, 10, 10, 1, 2, 9]

    root = tuple(int(row[0][0] == 1) for row in H397.rules)
    levels = (root, next_activity(root), next_activity(next_activity(root)))
    assert levels == ((1, 1, 1, 0, 0, 0), (0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 0, 0))
    assert next_activity(levels[2]) == levels[1]
    assert all(sum(activity[mode] for mode in section) % 2 for activity in levels)

    # Count each edge carry over a whole cycle of occupied k-bit prefixes.
    # One occurrence of a mode sees both extensions of every shorter word.
    counts = [section.count(mode) for mode in range(6)]
    for k in range(1, 21):
        counts = [
            sum(counts[mode] for mode, row in enumerate(H397.rules)
                for _, outgoing in row if outgoing == target)
            for target in range(6)
        ]
        base = (21, 1, 1, 21, 1, 1) if k % 2 else (3, 21, 21, 3, 21, 21)
        assert counts == [n * 3 ** ((k - 1) // 2) for n in base]

    # Independently exercise the all-depth argument at the first ten levels.
    for k in range(1, 11):
        tail = [0] * k
        seen = set()
        traffic = 0
        for _ in range(1 << k):
            key = tuple(tail)
            assert key not in seen
            seen.add(key)
            for mode in section:
                traffic += propagate(tail, mode) != -1
        assert not any(tail)
        assert traffic == (46 if k % 2 else 90) * 3 ** ((k - 1) // 2)
    print('Pass 64, 29 occupied suffix bits, first phase-aligned return after 1024 sweeps.')
    print(f'Tail return word: {section_word}')
    print('Odd swap parity at every depth; explicit orbit checks through ten bits.')


if __name__ == '__main__':
    main()
