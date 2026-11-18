"""Finite, reproducible checks for the BB(2,5) research log. Python 3.10+.

Run python3 bb25_audit.py next to BB2x5_Rocq_holdouts_37.txt.
Every TM check uses the literal transition encoding and an unbounded sparse tape.
The interpreter's work limit raises an exception. A timeout never counts as a halt.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import re

PARITY = "1RB2LA1LA4RA2LA_0LA3RB3LB2RB---"
TERNARY = "1RB2LA4RA1LA3LA_0LA2RB3RB2LB---"
TERNARY_CLOSE = "1RB2LA4RA1LA3LA_0LA3RB3LB2RB---"
TERNARY_OPEN = "1RB2LA3LA4RA1LA_0LA3LB3RB1RB---"
COUNTER = "1RB2RB4LA2RA1LA_2LA4RA3LA---3RA"
ARITHMETIC = "1RB3LA1LA1RA1RA_2LB2RA---4RB1LB"


def parse(encoding):
    row_pattern = r"(?:(?:[0-4][LR][AB]|---){5})"
    if not re.fullmatch(row_pattern + "_" + row_pattern, encoding):
        raise ValueError(encoding)
    rules = {}
    for state, row in zip("AB", encoding.split("_")):
        for symbol in range(5):
            token = row[3*symbol:3*symbol+3]
            if token != "---":
                rules[state, symbol] = int(token[0]), {"L": -1, "R": 1}[token[1]], token[2]
    return rules


class TapeMachine:
    def __init__(self, encoding, word=(), head=0, left=0):
        self.rules = parse(encoding)
        self.tape = {left+i: digit for i, digit in enumerate(word) if digit}
        self.head = head
        self.state = "A"
        self.steps = 0

    def step(self):
        read = self.tape.get(self.head, 0)
        rule = self.rules.get((self.state, read))
        if rule is None:
            return False
        write, move, self.state = rule
        if write:
            self.tape[self.head] = write
        else:
            self.tape.pop(self.head, None)
        self.head += move
        self.steps += 1
        return True

    def at_left_word(self, alphabet, terminal=None):
        if self.state != "A" or not self.tape or self.tape.get(self.head, 0):
            return None
        left = min(self.tape)
        if left != self.head + 1 or max(self.tape) != left + len(self.tape) - 1:
            return None
        word = [self.tape[left+i] for i in range(len(self.tape))]
        if terminal is not None and word[-1] != terminal:
            return None
        body = word if terminal is None else word[:-1]
        return word if all(digit in alphabet for digit in body) else None


def direct_epoch(machine, alphabet, terminal=None, limit=100_000):
    """First later normal form, or the actual undefined instruction."""
    for _ in range(limit):
        if not machine.step():
            return None
        result = machine.at_left_word(alphabet, terminal)
        if result is not None:
            return result
    raise RuntimeError("Direct interpreter exhausted its work limit")


@dataclass(frozen=True)
class SweepRules:
    opening: int
    marker: int
    ground: int
    capacity: int
    wall: tuple
    ternary_digits: tuple


SWEEPS = {
    PARITY: SweepRules(1, 3, 2, 2, (1, 3, 3, 4), ()),
    TERNARY: SweepRules(1, 2, 3, 2, (1, 3, 4), (3, 1, 2)),
    TERNARY_CLOSE: SweepRules(1, 3, 2, 2, (3, 4), (3, 1, 2)),
    TERNARY_OPEN: SweepRules(2, 3, 1, 0, (1, 4), (1, 2, 3)),
}


def word_sweep(word, encoding):
    """Exact normalized return. The minimum includes the empty prefix."""
    rules = SWEEPS[encoding]
    marker, ground = rules.marker, rules.ground
    row = [1]
    unmatched = []
    guard_uses = 0
    reset = False
    height = low = 0
    for digit in word:
        if digit == rules.opening:
            height += 1
            unmatched.append(len(row))
            row.append(marker)
        elif digit == ground:
            height -= 1
            low = min(low, height)
            if unmatched:
                row[unmatched.pop()] = ground
                row.append(ground)
            elif guard_uses < rules.capacity:
                guard_uses += 1
                row[0] = marker if guard_uses == 1 else ground
                row.append(ground)
            elif reset:
                assert low == -2*(rules.capacity+1)
                return None, low
            else:
                reset = True
                guard_uses = 0
                row = [1] + [ground] * (len(row) + 1)
        elif rules.ternary_digits and digit == marker:
            row.append(ground)
        else:
            raise ValueError(digit)
    if reset:
        row = list(rules.wall) + row
    result = []
    carry = 0
    for digit in row:
        if not rules.ternary_digits:
            value = 1 if digit == 2 else 2
            result.append(3-value if carry else value)
            carry = int(digit == 3)
        else:
            # The old wall 4 writes the zero digit without passing a carry.
            base = 0 if digit == 4 else rules.ternary_digits.index(digit)+1
            value = base + carry
            result.append(rules.ternary_digits[value % 3])
            carry = value // 3
    if carry:
        result.append(2)
    return result, low


def textword(word):
    return "".join(map(str, word))


def digits(word):
    return list(map(int, word))


def check_reset_trace(encoding, expected):
    machine = TapeMachine(encoding)
    visits = []
    for _ in range(32):
        if machine.head == 1:
            assert machine.tape.get(1, 0) == 0
            assert max(machine.tape) < 1
            left_word = [machine.tape.get(i, 0) for i in range(min(machine.tape), 1)]
            visits.append((machine.steps, machine.state, textword(left_word)))
            if machine.state == "A":
                break
        assert machine.step()
    assert visits == expected


def check_word_sweeps(encoding, max_length):
    rules = SWEEPS[encoding]
    alphabet = (1, 2, 3) if rules.ternary_digits else (1, 2)
    tally = Counter()
    for size in range(max_length+1):
        for word in product(alphabet, repeat=size):
            expected, low = word_sweep(word, encoding)
            machine = TapeMachine(encoding, word, left=1)
            actual = direct_epoch(machine, alphabet)
            assert expected == actual, (encoding, word, expected, actual)
            if actual is None:
                assert (machine.state, machine.tape.get(machine.head, 0)) == ("B", 4)
            tally[low] += 1
    # Independently follow the first 64 whole epochs from the blank tape.
    machine = TapeMachine(encoding)
    word = []
    for _ in range(64):
        word, _ = word_sweep(word, encoding)
        assert word is not None and direct_epoch(machine, alphabet) == word
    threshold = -2*(rules.capacity+1)
    print(f"word sweep {encoding}: {sum(tally.values())} inputs, {tally[threshold]} halting inputs; "
          f"64 blank epochs cross-checked at concrete step {machine.steps}")
    word = []
    minima = Counter()
    for _ in range(2000):
        word, low = word_sweep(word, encoding)
        assert word is not None
        if encoding in (TERNARY_CLOSE, TERNARY_OPEN):
            assert word[-1] == 2
        minima[low] += 1
    print(f"  2000 blank epochs: final width {len(word)}, prefix minima {dict(sorted(minima.items()))}")


def counter_trip(word):
    """B at the first of aligned pairs; include the return through the visited pairs."""
    rebuilt = []
    for i in range(0, len(word), 2):
        first = word[i]
        if first == 3:
            return None
        second = word[i+1]
        if second == 3:
            return rebuilt + [first, 4 if first == 1 else 1, 4, 3]
        if (first, second) == (1, 4):
            return rebuilt + [1, 1] + word[i+2:]
        rebuilt.extend((1, 4) if first == 1 else (first, second))
    raise ValueError("Missing terminal 3")


def counter_epoch(word):
    for _ in range(2):
        word = counter_trip(word)
        if word is None:
            return None
    return [4] + word


def column_token(state, token):
    """Occupied state (odd bit, even bit). Return new state and emitted token."""
    odd, even = state
    if token == "d":
        return (odd, even ^ odd), "d" if not odd or even else ""
    if token not in ("a", "b"):
        raise ValueError(token)
    output = ("a", "b")[even] if token == "a" or odd else ""
    return (odd ^ int(token == "b"), even), output


def feed_columns(columns, token):
    for index, state in enumerate(columns):
        columns[index], token = column_token(state, token)
        if not token:
            return True
    if token == "d":
        return False
    columns.append((int(token == "a"), 0))
    return True


def next_period(word):
    if word[0] == "d":
        raise ValueError("Dangerous first token at a fresh column")
    initial = (1, 0)
    state = initial
    raw = []
    for _ in range(4):
        for token in word:
            state, output = column_token(state, token)
            if output:
                raw.append(output)
        if state == initial:
            assert raw[0] == "a"
            return "".join(raw[1:]) + "a"
    raise AssertionError("Occupied state did not return after four input periods")


def check_counter():
    count = halts = 0
    for size in range(9):
        for body in product((1, 4), repeat=size):
            word = list(body) + [3]
            expected = counter_epoch(word)
            machine = TapeMachine(COUNTER, word, left=1)
            actual = direct_epoch(machine, (1, 4), terminal=3)
            assert actual == expected, (word, expected, actual)
            if expected is None:
                assert (machine.state, machine.tape.get(machine.head, 0)) == ("B", 3)
                halts += 1
            count += 1
    machine = TapeMachine(COUNTER)
    word = direct_epoch(machine, (1, 4), terminal=3)
    assert word == [4, 3] and machine.steps == 5
    columns = []
    for n in range(1, 301):
        word = counter_epoch(word)
        assert word is not None
        for _ in range(2):
            assert feed_columns(columns, "a" if n % 2 else "d")
        decoded = [4]*(n+1) + [1 if bit else 4 for col in columns for bit in col] + [3]
        assert word == decoded
        if n <= 64:
            assert direct_epoch(machine, (1, 4), terminal=3) == word
    print(f"counter: {count} direct epoch checks, {halts} halting inputs; "
          f"300 blank epochs vs column model, first 64 vs concrete TM after entry")
    period = "aadd"
    starts = []
    for j in range(13):
        starts.append(period[0])
        if j <= 3:
            assert period == ("aadd", "ada", "bbdaa", "bbbdaaa")[j]
        else:
            scale = 3**(j-3)
            assert Counter(period) == {"a": 3*scale, "b": 3*scale, "d": scale}
        if j < 12:
            period = next_period(period)
    assert next_period("bdaaabb").startswith("d")
    print(f"  stream representatives j=0..12: first tokens {''.join(starts)}, last length {len(period)}")


def arithmetic_form(tag, a, b):
    if tag == "A":
        left = "1" + "4"*a + "1111"
        right = "1"*b + "2"
    else:
        left = "1" + "4"*a + "1"*(3+b)
        right = "11"
    return digits(left+right), len(left)


def published_return(tag, a, b):
    if tag == "A":
        if b >= a+3:
            return "A", 2*a+4, b-a-3
        if b == a+2:
            return "B", 2*a+2, 3
        if b == a+1:
            return None
        return "B", a-b, 2*b
    base, residue = divmod(a, 3)
    if residue == 1:
        return "A", 4, 2+5*base+b
    if residue == 2:
        return "B", 5+5*base+b, 2
    return "B", 3+5*base+b, 0


def audit_arithmetic_transition(start, target):
    word, head = arithmetic_form(*start) if start else ([], 0)
    machine = TapeMachine(ARITHMETIC, word, head=head)
    if target:
        goal, new_head = arithmetic_form(*target)
    for _ in range(100_000):
        if not machine.step():
            assert target is None
            return machine.steps
        if (target and machine.state == "A" and len(machine.tape) == len(goal)
            and all(machine.tape.get(machine.head+i-new_head, 0) == a for i, a in enumerate(goal))):
            return machine.steps
    raise RuntimeError("Arithmetic transition audit exhausted its work limit")


def largest_repeat(b):
    k = max(0, b.bit_length()-3)
    while k and 8*((1<<k)-1)-k > b:
        k -= 1
    while 8*((1<<(k+1))-1)-(k+1) <= b:
        k += 1
    return k


def check_arithmetic():
    assert audit_arithmetic_transition(None, ("A", 4, 4)) == 136
    for tag, a, b in product("AB", range(12), range(18)):
        audit_arithmetic_transition((tag, a, b), published_return(tag, a, b))
    b = 4
    samples = []
    for _ in range(1024):
        samples.append(b)
        k = largest_repeat(b)
        state = published_return("A", 8*(1<<k)-4, b-8*((1<<k)-1)+k)
        assert state is not None
        while state[0] == "B":
            state = published_return(*state)
        tag, a, b = state
        assert tag == "A" and a == 4
    assert samples[:4] == [4, 64, 104, 569]
    assert {v % 64 for v in samples} == set(range(64))
    print(f"arithmetic: blank entry at step 136; 432 direct rule instances; "
          f"1024 sampled A(4,b) values cover all 64 residues; last has {samples[-1].bit_length()} bits")


def main():
    if not __debug__:
        raise SystemExit("Run without -O so that all audit assertions are active")
    listed = Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt").read_text().splitlines()
    assert len(listed) == len(set(listed)) == 37
    for encoding in listed:
        assert len(parse(encoding)) == 9
    for pos, encoding in [(36, PARITY), (34, TERNARY), (35, TERNARY_CLOSE), (37, TERNARY_OPEN),
                          (26, COUNTER), (5, ARITHMETIC)]:
        assert listed[pos-1] == encoding
    print("37 distinct well-formed encodings, all with one undefined instruction")
    check_reset_trace(PARITY, [(1, "B", "1"), (7, "B", "32"), (21, "B", "222"),
                               (29, "B", "1333"), (31, "A", "1334")])
    check_reset_trace(TERNARY, [(1, "B", "1"), (5, "B", "13"), (11, "B", "132"),
                                (13, "A", "134")])
    check_reset_trace(TERNARY_CLOSE, [(1, "B", "1"), (7, "B", "32"), (9, "A", "34")])
    check_reset_trace(TERNARY_OPEN, [(1, "B", "1"), (5, "B", "13"), (7, "A", "14")])
    for encoding in SWEEPS:
        check_word_sweeps(encoding, 11 if encoding == PARITY else 7)
    counterexample, low = word_sweep(digits("1121121121"), PARITY)
    assert low == 0 and textword(counterexample) == "222122122122"
    assert word_sweep(counterexample, PARITY) == (None, -6)
    # The entire two-epoch counterexample also runs directly on the concrete TM.
    machine = TapeMachine(PARITY, digits("1121121121"), left=1)
    assert direct_epoch(machine, (1, 2)) == counterexample
    assert direct_epoch(machine, (1, 2)) is None
    print(f"nonblank two-epoch counterexample reaches B4 at concrete step {machine.steps}")
    # A periodic input chosen by a circular-word search. Check its concrete boundary.
    word = digits("111112211122112") * 15
    machine = TapeMachine(PARITY, word, left=1)
    lows = []
    for _ in range(9):
        word, low = word_sweep(word, PARITY)
        lows.append(low)
        assert direct_epoch(machine, (1, 2)) == word
    assert lows == [0, -2, 0, -1, -3, -2, 0, -3, -6] and word is None
    print(f"longer nonblank witness: eight safe epochs; B4 at concrete step {machine.steps}")
    # A boundary-compatible derivative shape for the capacity-zero ternary machine.
    old_bits = [0] + digits("011000110001")
    body = [2 if x == y else (1 if y else 3) for x, y in zip(old_bits, old_bits[1:])]
    word = [2] + body + [2]
    machine = TapeMachine(TERNARY_OPEN, word, left=1)
    first, low = word_sweep(word, TERNARY_OPEN)
    assert low == 0 and textword(first) == "2132131321313212"
    assert direct_epoch(machine, (1, 2, 3)) == first
    assert word_sweep(first, TERNARY_OPEN) == (None, -2)
    assert direct_epoch(machine, (1, 2, 3)) is None
    check_counter()
    check_arithmetic()


if __name__ == "__main__":
    main()
