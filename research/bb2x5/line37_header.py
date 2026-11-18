"""Finite left-prefix implications for line 37, conditional on the stated debt bounds."""

from itertools import product
from pathlib import Path

from prior_sweeps import TERNARY_OPEN, word_sweep


def prefix_masks(word):
    openings = closings = 0
    for symbol in word:
        openings = (openings << 1) | (symbol == 2)
        closings = (closings << 1) | (symbol == 1)
    return openings, closings


def prefix_images(state, width, cut_cap, interior_cap=None):
    """Yield the successor prefix and guard debt, or (None, debt) for a halt."""
    openings, closings = state
    survivors = 0
    debt = imbalance = peak = 0
    allowed = cut_cap
    for i in range(width):
        bit = 1 << i  # the rightmost digit of the prefix is least significant
        if closings & bit:
            debt += 1
            imbalance += 1
        elif openings & bit:
            imbalance -= 1
            if debt:
                debt -= 1
            else:
                survivors |= bit
        peak = max(peak, debt)
        if interior_cap is not None:
            allowed = min(allowed, interior_cap - imbalance)
    if interior_cap is not None and peak > interior_cap:
        return

    mask = (1 << width) - 1
    for _ in range(allowed + 1):
        if debt >= 2:
            yield None, debt
            return
        previous = survivors >> 1
        data_openings = ~(survivors ^ previous) & mask
        data_closings = survivors & ~previous
        if debt:
            # One guard reset prefixes 2122. There is at least one old digit.
            yield ((data_openings >> 4) | (0b1011 << (width - 4)),
                   (data_closings >> 4) | (0b0100 << (width - 4))), debt
        else:
            yield ((data_openings >> 1) | (1 << (width - 1)), data_closings >> 1), debt

        # Increasing the chosen exterior debt by one either cancels the
        # rightmost surviving opening or reaches the left guard.
        if survivors:
            survivors &= survivors - 1
        else:
            debt += 1


def audit_images():
    for width in range(4, 7):
        for prefix in product((1, 2, 3), repeat=width):
            for cap in range(4):
                for interior_cap in (None, 3):
                    expected = set()
                    for initial in range(cap + 1):
                        debt = initial
                        peak = initial
                        for symbol in reversed(prefix):
                            debt = max(0, debt + (symbol == 1) - (symbol == 2))
                            peak = max(peak, debt)
                        if interior_cap is not None and peak > interior_cap:
                            continue
                        # A canonical exterior realizing exactly this cut debt.
                        word = prefix + (1,) * initial + (2,)
                        successor, _ = word_sweep(word, TERNARY_OPEN)
                        expected.add(None if successor is None else prefix_masks(successor[:width]))
                    actual = {s for s, _ in prefix_images(prefix_masks(prefix), width, cap, interior_cap)}
                    assert actual == expected


def closure(word, width, cut_cap, interior_cap, check_phase=False):
    seed = prefix_masks(word[:width])
    visited = {seed: 91 % 11}
    queue = [seed]
    while queue:
        next_layer = []
        for state in queue:
            phase = visited[state]
            for successor, guard_debt in prefix_images(state, width, cut_cap, interior_cap):
                assert successor is not None
                next_phase = (phase + 1) % 11
                if check_phase:
                    assert guard_debt == int(phase == 1)
                    assert visited.get(successor, next_phase) == next_phase
                if successor not in visited:
                    visited[successor] = next_phase
                    next_layer.append(successor)
        queue = next_layer
    return len(visited)


def main():
    assert Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[36] == TERNARY_OPEN
    audit_images()
    word = []
    for _ in range(91):
        word, _ = word_sweep(word, TERNARY_OPEN)
        assert word is not None
    for width, exterior, interior, count in [(45, 4, None, 58302), (40, 5, 5, 26007), (48, 6, 6, 196262)]:
        assert closure(word, width, exterior, interior, check_phase=interior is None) == count
        domain = f'first {width} cells and cut' if interior is not None else f'cut {width} only'
        print(f'Debt at most {exterior} ({domain}): {count} safe reachable prefixes.')
        if interior is None:
            print('  A guard reset occurs exactly at epochs congruent to 1 modulo 11.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    main()
