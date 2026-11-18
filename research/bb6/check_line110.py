"""Compare the visit recurrence with literal steps of stable line 110."""
from pathlib import Path

from line110_visits import Halt, blank, visits
from tracker import load_register


def run_until(table, ones, head, state, goal, limit, scanned=None):
    for steps in range(limit + 1):
        instruction = table[state][int(head in ones)]
        if instruction == "---":
            return None
        if (head, state) == goal and (scanned is None or int(head in ones) == scanned):
            return steps
        if instruction[0] == "1":
            ones.add(head)
        else:
            ones.discard(head)
        head += 1 if instruction[1] == "R" else -1
        state = instruction[2]
    raise RuntimeError(f"literal replay exceeded {limit} steps")


def cells(word):
    return {i for i in range(word.bit_length()) if word & (1 << i)}


def test():
    row = load_register()[109]
    source = Path(__file__).with_name("Line110Visits.v").read_text()
    assert row["machine_id"] == "28035" and f'"{row["machine"]}"' in source
    table = {chr(65 + i): (s[:3], s[3:]) for i, s in enumerate(row["machine"].split("_"))}
    cases = halts = 0
    for word in range(256):
        for requests in range(1, 6):
            ones = cells(word)
            elapsed = 0
            for _ in range(requests):
                result = run_until(table, ones, 0, "C", (-2, "A"), 10000)
                if result is None:
                    break
                elapsed += result
            try:
                expected, cost = visits(word, requests)
            except Halt:
                assert result is None, (word, requests)
                halts += 1
            else:
                assert result is not None and cost == elapsed and cells(expected) == ones, (word, requests)
            cases += 1
    print(f"{cases} guarded inputs matched, including {halts} halts")

    # At a root return the left tape is blank, the head reads 1 and a 0
    # separates it from the suffix. Check every cell as well as the raw clock.
    # A at a coordinate can appear earlier with a different tape; use the
    # formal visit's C entry and its first A return to distinguish the event.
    ones = set()
    head = 2
    total = run_until(table, ones, 0, "A", (head, "C"), 10)
    for n in range(1, 25):
        delta = run_until(table, ones, head, "C", (head - 2, "A"), 1000000)
        total += delta
        head -= 2
        count, suffix, clock = blank(n)
        assert count == n and total == clock
        assert ones == {head} | {head + 2 + i for i in cells(suffix)}
        if n < 24:
            total += run_until(table, ones, head, "A", (head, "C"), 10, scanned=1)
    print(f"24 blank root returns matched cell for cell through {total:,} instructions")


if __name__ == "__main__":
    test()
