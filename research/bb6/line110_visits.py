"""Batched blank runs of BB(6) line 110. Bit zero is the first cell of a word."""
import argparse
import hashlib


class Halt(Exception):
    """A requested visit reached F reading one."""


def visits(word, count):
    """Return the suffix and literal cost after count complete visits, or raise Halt."""
    if word < 0 or count < 0:
        raise ValueError("word and visit count must be nonnegative")
    output = used = cost = 0
    pending = []
    while True:
        if count == 0:
            result = output | (word << used)
            if not pending:
                return result, cost
            # The two inner visits in 11100 have finished. Visit 10 + result.
            output, used, count = pending.pop()
            word = 1 | (result << 2)
            continue
        if word & 4 == 0:
            # For either b00 or b10, every second visit carries into the suffix.
            first = word & 1
            carries = (count + first) // 2
            if carries == 0:
                word |= 1
                cost += 2
                count = 0
                continue
            cost += 2 * (count - carries) + 6 * carries + (word & 2)
            output |= ((first + count) & 1) << used
            used += 3
            word >>= 3
            count = carries
            continue
        if word & 1 == 0:
            word |= 1
            count -= 1
            cost += 2
            continue
        if word & 15 == 5:
            # Each 1010 doubles all requests. Find the whole alternating prefix.
            difference = word ^ (word >> 2)
            matching = (difference & -difference).bit_length() + 1
            blocks = matching // 4
            width = 4 * blocks
            output |= (word & ((1 << width) - 1)) << used
            used += width
            word >>= width
            doubled = count << blocks
            cost += 16 * (doubled - count)
            count = doubled
            continue
        if word & 15 == 13:  # 1011 returns 0001
            word &= ~7
            count -= 1
            cost += 14
            continue
        if word & 15 == 15:  # 1111 reaches F1
            raise Halt
        if word & 16:  # 11101 returns 10101
            word &= ~2
            count -= 1
            cost += 18
            continue

        # 11100 u returns 000 V(10 V(V(u))). The remaining requests see 000.
        remaining = count - 1
        carries = remaining // 2
        cost += 16 + 2 * (remaining - carries) + 6 * carries
        output |= (remaining & 1) << used
        pending.append((output, used + 3, 1 + carries))
        output = used = 0
        word >>= 5
        count = 2


def blank(rounds):
    """Stop just after the requested root return, in A, with its full right word."""
    if rounds < 1:
        raise ValueError("at least one root return is required")
    word, steps = 0, 2  # blank A reaches the first guarded C
    for turn in range(1, rounds + 1):
        try:
            word, cost = visits(word, 1)
        except Halt:
            return turn, None, None
        steps += cost
        if turn < rounds:
            word = 1 | (word << 2)
            steps += 6
    return rounds, word, steps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rounds", type=int)
    args = parser.parse_args()
    if args.rounds < 1:
        parser.error("rounds must be positive")
    turn, word, steps = blank(args.rounds)
    if word is None:
        print(f"F1 reached during root visit {turn}")
        return
    size = word.bit_length()
    data = word.to_bytes((size + 7) // 8, "little")
    print(f"root returns: {turn}; state: A; head: {2 - 2 * turn}")
    print(f"suffix bits through its last one: {size}; ones: {word.bit_count()}")
    print(f"suffix SHA-256 (little endian, zero-padded final byte): {hashlib.sha256(data).hexdigest()}")
    print(f"defined steps, hexadecimal: {steps:#x}")


if __name__ == "__main__":
    main()
