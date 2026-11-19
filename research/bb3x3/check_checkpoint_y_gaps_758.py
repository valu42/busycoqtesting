"""Check the contact points joining the last annular cell to the Y gate chain."""
from pathlib import Path

from annular_skip_758 import partition
from check_bb33 import HALTING_TARGET, first_return

HERE = Path(__file__).resolve().parent
POWER = 3**292
Y = 3**301 // 19171 + 4510976


def read(name):
    return [tuple(map(int, line.split())) for line in (HERE / name).read_text().splitlines()]


def main():
    cells = [(lo, hi) for lo, hi, *rules in partition(POWER, 8)
             if lo < HALTING_TARGET and None not in rules]
    assert len(cells) == 11
    first, original_end = cells[-1]
    assert original_end == Y - 4511571
    gains = [first_return(s) - s for s in range(original_end, Y - 4500000)]
    assert (len(gains), min(gains), max(gains)) == (11571, 605, 3455)

    cover = read('checkpoint_y_gaps_758.tsv')
    assert cover[0][:2] == (-4500000, 0)
    gates = read('checkpoint_y_758.tsv')
    prior_end = 0
    for row, gate in zip(cover[1:], gates):
        lo, hi, nodes, leaves, bound = row
        _, gate_lo, gate_hi, *_ = gate
        assert (lo, hi) == (prior_end, gate_lo)
        assert (nodes, nodes % 2) == (2 * leaves - 1, 1)
        assert 615 <= bound < gate_hi - gate_lo
        prior_end = gate_hi
    assert 1 < len(cover) <= len(gates) + 1
    assert 3455 < 4500000 and cover[0][-1] < gates[0][1]
    last = Y + prior_end - 1
    decrease, right = 0, 1
    for _ in range(785):
        q = (right + 1) // 4
        decrease += 4*q + 3
        right = 6*q + 5
    assert decrease - 6 <= 2*first + 1
    assert 2*last + 1 <= decrease + right - 6
    ordinary_calls = (2*(last-first) - 5465 + 8) // 9
    assert ordinary_calls > 533 * 10**133
    print(f'Every seed from {first} through Y+{prior_end-1:,} reaches Y+{gates[-1][-1]:,}.')
    print(f'Contiguous interval size {Y+prior_end-first:,}.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
