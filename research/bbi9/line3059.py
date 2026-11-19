"""Replay BBi(9) 3x5 holdout 3059 exactly, using blocks of adjacent tape cells."""

import argparse
from functools import lru_cache
from pathlib import Path


MACHINE = "1RB0LC3RA------_1RC2RA---------_1LA0RB4RA1LC---"
RULES = {}
for state, row in zip("ABC", MACHINE.split("_")):
    for symbol in range(5):
        code = row[3 * symbol:3 * symbol + 3]
        if code != "---":
            RULES[state, symbol] = int(code[0]), (1 if code[1] == "R" else -1), code[2]


@lru_cache(maxsize=None)
def cross(original, state, direction):
    """Interpret the actual cells until the head exits this block or encounters a halt."""
    word = bytearray(original)
    offset = 0 if direction == 1 else len(word) - 1
    steps = 0
    while 0 <= offset < len(word):
        rule = RULES.get((state, word[offset]))
        if rule is None:
            break
        write, move, state = rule
        word[offset] = write
        offset += move
        steps += 1
    return bytes(word), state, offset, steps


def push(stack, word, count):
    # Runs are stored farthest first. An empty stack already represents blank space.
    if not stack and not any(word):
        return
    if stack and stack[-1][0] == word:
        stack[-1] = (word, stack[-1][1] + count)
    else:
        stack.append((word, count))


def consume(stack, count):
    if not stack:
        return
    word, length = stack[-1]
    if count == length:
        stack.pop()
    else:
        stack[-1] = (word, length - count)


def final_tape(left, right, boundary, width):
    first_cell = (boundary - sum(n for _, n in left)) * width
    raw = b"".join(word * n for word, n in left)
    raw += b"".join(word * n for word, n in reversed(right))
    trimmed_left = raw.lstrip(b"\x00")
    support = trimmed_left.rstrip(b"\x00")
    leftmost = first_cell + len(raw) - len(trimmed_left) if support else 0
    return leftmost, support


def run(width):
    blank = bytes(width)
    left, right = [], []
    # Block boundary b separates blocks b-1 and b. Start at cell 0 facing right.
    boundary, direction, steps, state = 0, 1, 0, "A"
    while True:
        source, other = (right, left) if direction == 1 else (left, right)
        word, length = source[-1] if source else (blank, 1)
        new_word, next_state, offset, cost = cross(word, state, direction)
        if 0 <= offset < width:
            consume(source, 1)
            push(source, new_word, 1)
            block = boundary if direction == 1 else boundary - 1
            head = width * block + offset
            leftmost, support = final_tape(left, right, boundary, width)
            return steps + cost, next_state, new_word[offset], head, leftmost, support

        exit_direction = 1 if offset == width else -1
        through = exit_direction == direction
        repeated = through and next_state == state
        count = length if repeated else 1
        consume(source, count)
        push(other if through else source, new_word, count)
        if through:
            boundary += direction * count
        steps += cost * count
        direction, state = exit_direction, next_state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, choices=(2, 4, 8), default=2)
    parser.add_argument("--tape", type=Path, help="write the complete tape between its support bounds")
    args = parser.parse_args()
    steps, state, read, head, leftmost, support = run(args.width)
    print(f"defined steps {steps}\nundefined entry {state}{read}\nhead {head}")
    print(f"support bounds {leftmost} {leftmost + len(support) - 1}")
    print("symbols 1-4", *(support.count(bytes([s])) for s in range(1, 5)))
    if args.tape:
        printable = bytes.maketrans(bytes(range(5)), b"01234")
        args.tape.write_bytes(support.translate(printable) + b"\n")
