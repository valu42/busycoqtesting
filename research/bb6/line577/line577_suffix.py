"""Check two sufficient local terminal conditions for BB(6) line 577."""
import argparse
from pathlib import Path

from line577_replay import REFERENCE, WALL, glider_patterns, rule_source
from line577_rules import H_LEFT, H_RIGHT

def call(right, patterns):
    # All cells below -len(H_LEFT) are unknown. The right tail is blank.
    low = -len(H_LEFT)
    ones = {j for j, v in zip(range(low, 0), reversed(H_LEFT)) if v == "1"}
    ones.update(i for i, v in enumerate(right) if v == "1")
    state, head = "D", 0
    for elapsed in range(3000):
        if head < low:
            assert head == low - 1
            bits = "".join("1" if i in ones else "0" for i in range(low, max(ones, default=low) + 1))
            if state == "A" and bits.startswith(H_RIGHT):
                return "return", bits[len(H_RIGHT):], elapsed
            return "outside", None, elapsed
        for left, right_bits, phase in patterns.get(state, []):
            if head - len(left) < low or max(ones, default=head - 1) >= head + len(right_bits):
                continue
            if any((head - i - 1 in ones) != (b == "1") for i, b in enumerate(left)):
                continue
            if all((head + i in ones) == (b == "1") for i, b in enumerate(right_bits)):
                return "glider", phase, elapsed
        bit = int(head in ones)
        instruction = REFERENCE[ord(state) - 65][3 * bit:3 * bit + 3]
        if instruction == "---":
            assert state == "E" and bit == 1
            return "halt", None, elapsed
        value, move, state = instruction
        if value == "1":
            ones.add(head)
        else:
            ones.discard(head)
        head += 1 if move == "R" else -1
    raise AssertionError("local call did not finish within its inspection bound")

def check(right, times, expected, patterns):
    subtotal = 0
    for count in range(1, times + 1):
        result, value, steps = call(right, patterns)
        subtotal += steps
        if count == times:
            assert result == expected, (result, expected)
            print(result, "on call", count, "after", subtotal, "moves inside calls")
            return
        assert result == "return"
        right = value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean_source", type=Path)
    args = parser.parse_args()
    digits, _, _ = rule_source(args.lean_source)
    patterns = glider_patterns()
    check(digits[7] + WALL * 2 + digits[18] + WALL + "1", 25, "halt", patterns)
    check(digits[18] + "1", 8, "glider", patterns)
    check(digits[18] + WALL + "1", 4, "outside", patterns)
