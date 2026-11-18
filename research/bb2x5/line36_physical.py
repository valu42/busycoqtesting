"""Run with prior_sweeps.py on PYTHONPATH and assertions enabled."""
from collections import Counter
from itertools import product

from prior_sweeps import PARITY, TapeMachine, direct_epoch, word_sweep


HEADER = ("2", "2", "1", "221121", "221122", "221111")


def derivative(word):
    """Use right-to-left debt, then the six possible physical headers."""
    debt = 0
    survivors = []
    for digit in reversed(word):
        survives = digit == 1 and debt == 0
        survivors.append(survives)
        debt = max(0, debt + (1 if digit == 2 else -1))
    if debt >= 6:
        return debt, None
    previous = debt == 1
    output = list(map(int, HEADER[debt]))
    for survives in reversed(survivors):
        output.append(1 + (previous != survives))
        previous = survives
    if previous:
        output.append(2)
    return debt, output


def check_reset():
    machine = TapeMachine(PARITY, (3,), left=1)
    machine.state = "B"
    visits = []
    while machine.steps < 33:
        if machine.head == 0:
            left = min((x for x in machine.tape if x < 0), default=0)
            word = "".join(str(machine.tape.get(x, 0)) for x in range(left, 0))
            assert machine.tape.get(0, 0) == 0
            visits.append((machine.steps, machine.state, word))
        assert machine.head <= 0 and machine.step()
    assert visits == [(0, "B", ""), (2, "B", "1"), (8, "B", "32"),
                      (22, "B", "222"), (30, "B", "1333"), (32, "A", "1334")]
    assert machine.state == "B" and machine.head == 1
    assert machine.tape == dict(zip(range(-4, 2), (1, 3, 3, 4, 1, 3)))


def main():
    if not __debug__:
        raise SystemExit("Run with assertions enabled")
    check_reset()
    counts = Counter()
    for n in range(13):
        for word in product((1, 2), repeat=n):
            d, expected = derivative(word)
            symbolic, low = word_sweep(word, PARITY)
            assert symbolic == expected and low == -min(d, 6)
            machine = TapeMachine(PARITY, word, left=1)
            assert direct_epoch(machine, (1, 2)) == expected
            if expected is None:
                assert (machine.head, machine.state, machine.tape[machine.head]) == (-2, "B", 4)
            else:
                assert (machine.head, machine.state) == ((-6 if d >= 3 else -1), "A")
            counts[min(d, 6)] += 1
    print(sum(counts.values()), "finite inputs. Counts by 0 through 6 or more unmatched closings:",
          [counts[d] for d in range(7)])


if __name__ == "__main__":
    main()
