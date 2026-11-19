"""Verify the repeated return that starts at the published #758 checkpoint.

Each pass of the verifier checks an entire affine family of states. The variable
k enumerates returns; all arithmetic is integer. Run with Python 3.10+.
"""
from math import comb

from check_bb33 import champion_step
from timing_758 import branch_cost

PUBLISHED_C = 1_059_491_543_272_883
RETURNS = 254_074_710_616
END_C = 1_079_817_520_122_241


def guard(state):
    a, c = state
    if a <= c:
        return 0, a % 2, c % 2
    return min(a - c, 4), c % 4


def trace_family(start, stride, count):
    """Prove one return for every k from 0 through count-1 inclusive."""
    if count < 3:
        raise ValueError("the progression needs three distinct samples")
    indices = (0, 1, 2, count - 1)
    states = [(1, start + k * stride) for k in indices]
    times = [0] * len(indices)
    for step in range(1, 38):
        base, adjacent, _, last = states
        slope = tuple(y - x for x, y in zip(base, adjacent))
        for k, state in zip(indices, states):
            assert tuple(x + k * dx for x, dx in zip(base, slope)) == state
        # Guard inequalities describe intervals in k, hence endpoints suffice.
        # Equal residues at adjacent k make each required residue constant.
        assert all(guard(s) == guard(base) for s in states)
        if step > 1:
            assert min(base[0], last[0]) >= 2 or base[0] == last[0] == 0
        times = [t + branch_cost(*s) for t, s in zip(times, states)]
        states = [champion_step(*state) for state in states]
        assert all(state is not None for state in states)
    assert states == [(1, start + (k + 1) * stride) for k in indices]
    # On fixed guards each clock is quadratic in affine state coordinates.
    zero, one, two, last_time = times
    first, second = one - zero, two - 2*one + zero
    assert last_time == zero + (count-1)*first + comb(count-1, 2)*second
    return count*zero + comb(count, 2)*first + comb(count, 3)*second


def verify():
    state = (1, PUBLISHED_C)
    elapsed = 0
    for step in range(1, 100):
        elapsed += branch_cost(*state)
        state = champion_step(*state)
        assert state is not None
        if state[0] == 1:
            break
    assert state == (1, PUBLISHED_C + 78)
    elapsed += trace_family(state[1], 80, RETURNS)
    assert state[1] + RETURNS * 80 == END_C
    print(f"A(1,{PUBLISHED_C}) -> A(1,{END_C}) in {1 + RETURNS:,} returns "
          f"and {step + 37 * RETURNS:,} two-counter steps.")
    print(f"Exact raw transitions between these two checkpoints: {elapsed:,}.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to keep verification enabled.")
    verify()
