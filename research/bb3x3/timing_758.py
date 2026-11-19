#!/usr/bin/env python3
"""Raw #758 clocks for the two-counter rules in check_bb33.py.

Source: https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#A(a,_c)_Rules_and_Timings
Each terminal cost includes the final transition into halt, the BB step convention.
"""
from check_bb33 import Tape, champion_step


def branch_cost(a, c):
    """Number of original transitions until the next A configuration or halt."""
    if a <= c:
        if a % 2 == 0:
            if c % 2 == 0:  # g, halt
                return 3*a*a + 5*a + 9*c + 24
            return 3*a*a + 3*a + 5*c + 11  # h
        if c % 2 == 0:  # i
            return 3*a*a - 9*a + 14*c + 30
        return 3*a*a + 5*c + 6  # j

    if c % 2 == 0:  # a
        return 3*c*c + 8*c + 5
    if a == c + 1:  # f, halt
        return 3*c*c + 8*c + 6
    if c % 4 == 1:  # b
        return (6*c*c + 31*c + 37) // 2
    if a == c + 2:  # e
        return (6*c*c + 37*c + 63) // 2
    if a == c + 3:  # d, halt
        return (6*c*c + 43*c + 75) // 2
    return 3*c*c + 29*c + 65  # c


def cells_at_a(a, c):
    """Nonblank tape symbols relative to the head of configuration A(a,c)."""
    cells = {-a: 1}
    cells.update((i, 2) for i in range(1-a, 1))
    cells.update((2*i + 1, 2) for i in range(c))
    return cells


def audit():
    """Compare all 400 clocks/targets on 0 <= a,c < 20 with the raw machine."""
    continued = halted = 0
    for a in range(20):
        for c in range(20):
            target = champion_step(a, c)
            expected_time = branch_cost(a, c)
            raw = Tape(758)
            raw.state, raw.cells = 2, cells_at_a(a, c)
            if target is None:
                raw.run_to(expected_time - 1)
                assert (raw.state, raw.cells.get(raw.head, 0)) not in raw.table
                halted += 1
            else:
                raw.run_to(expected_time)
                assert raw.state == 2
                actual = {pos - raw.head: val for pos, val in raw.cells.items()}
                assert actual == cells_at_a(*target)
                continued += 1
    assert (continued, halted) == (332, 68)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so all assertions execute.")
    audit()
    a, c, raw_time = 0, 1, 2
    for _ in range(2**21):
        raw_time += branch_cost(a, c)
        a, c = champion_step(a, c)
    assert (a, c, raw_time) == (107, 5_090_319, 3_251_620_479_139_366_879)
    print(f"All 400 raw clocks matched. #758 reaches A({a},{c}) at step {raw_time:,}.")
