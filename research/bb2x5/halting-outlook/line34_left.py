"""Enumerate line 34 left-guard configurations. Run with Python 3.10+."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prior_sweeps import TERNARY, TapeMachine, direct_epoch, word_sweep

# Physical output left of the transformed old cells, indexed by guard debt.
HEADERS = ("2", "3", "1", "21321", "21332", "21311")


def masks(word):
    openings = closings = 0
    for value in word:
        openings = (openings << 1) | (value == 1)
        closings = (closings << 1) | (value == 3)
    return openings, closings


def digits(state, width):
    openings, closings = state
    return tuple(1 if openings & (1 << i) else 3 if closings & (1 << i) else 2
                 for i in reversed(range(width)))


def targets(state, width, cap):
    """Enumerate exterior debts in order, stopping at the first undefined sweep."""
    openings, closings = state
    mask = (1 << width) - 1
    survivors = debt = 0
    for i in range(width):
        bit = 1 << i
        if closings & bit:
            debt += 1
        elif openings & bit:
            if debt:
                debt -= 1
            else:
                survivors |= bit
    for _ in range(cap + 1):
        if debt >= 6:
            yield None, debt
            return
        header = HEADERS[debt]
        old_left = (survivors >> 1) | ((debt == 1) << (width - 1))
        data_open = ~(survivors ^ old_left) & mask
        data_close = survivors & ~old_left & mask
        a, b = masks(map(int, header))
        k = len(header)
        assert k < width
        yield ((a << (width - k)) | (data_open >> k),
               (b << (width - k)) | (data_close >> k)), debt
        # One extra closing from the exterior removes the rightmost survivor.
        if survivors:
            survivors &= survivors - 1
        else:
            debt += 1


def seed(epoch):
    machine = TapeMachine(TERNARY)
    word = []
    for _ in range(epoch):
        word, _ = word_sweep(word, TERNARY)
        assert direct_epoch(machine, (1, 2, 3)) == word
    assert machine.state == "A" and len(machine.tape) == len(word)
    assert machine.tape == {machine.head + 1 + i: v for i, v in enumerate(word)}
    return word, machine.steps, machine.head


def prefix_graph(width, epoch, cap, literal):
    word, steps, head = seed(epoch)
    start = masks(word[:width])
    states = [start]
    seen = {start}
    edges = set()
    min_balance = min_peak = width
    max_debt = cases = halts = 0
    for state in states:
        prefix = digits(state, width)
        balance = low = high = 0
        for symbol in prefix:
            balance += (symbol == 1) - (symbol == 3)
            low = min(low, balance)
            high = max(high, balance)
        min_balance = min(min_balance, balance)
        min_peak = min(min_peak, high)
        max_debt = max(max_debt, -low)
        for d, (next_state, guard) in enumerate(targets(state, width, cap)):
            cases += 1
            assert guard == max(-low, d - balance)
            witness = prefix + (3,) * d
            new, level = word_sweep(witness, TERNARY)
            assert ((None if new is None else masks(new[:width])), -level) == (next_state, min(guard, 6))
            if literal:
                machine = TapeMachine(TERNARY, witness, left=1)
                assert direct_epoch(machine, (1, 2, 3)) == new
                if new is None:
                    assert machine.state == "B" and machine.tape[machine.head] == 4
                else:
                    assert machine.head == -len(HEADERS[guard]) and machine.state == "A"
                    assert machine.tape == {machine.head + 1 + i: v for i, v in enumerate(new)}
            if next_state is None:
                halts += 1
            else:
                edges.add((state, next_state))
                if next_state not in seen:
                    states.append(next_state)
                    seen.add(next_state)
    result = (len(states), len(edges), cases, halts, min_balance, max_debt, min_peak)
    print(f"width {width}, seed epoch {epoch} / step {steps} / head {head}: {result}")
    return result


def main():
    assert (ROOT / "BB2x5_Rocq_holdouts_37.txt").read_text().splitlines()[33] == TERNARY
    assert TERNARY == "1RB2LA4RA1LA3LA_0LA2RB3RB2LB---"
    # In an unrestricted graph, width+6 guarantees a halting choice for every prefix.
    print("Tuple: states, safe edges, choices, halting choices, least balance, largest intrinsic debt, least peak.")
    assert prefix_graph(9, 7, 5, True) == (65, 346, 390, 0, 0, 1, 1)
    assert prefix_graph(12, 10, 18, True) == (352, 3452, 4099, 352, 0, 2, 0)
    assert prefix_graph(16, 13, 22, False) == (2149, 25135, 29111, 2149, -2, 2, 1)
    print("Literal canonical-completion checks: 4489; all 29111 width-16 cases compared to word_sweep.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Enable assertions (omit -O).")
    main()
