"""Search beyond the certified restarts. The output is experimental.

Tapes are two tuples of maximal (bit, length) runs, nearest first. Trailing
blanks are implicit. A transition returns the elapsed time, signed movement,
and the name of its rule along with the entire new configuration.
"""
import argparse
import sys
from functools import cache

from certificate import Certificate

TABLE = ("1RB0LA", "1RC---", "0LD1RD", "0RA0RE", "0RF1RC", "1LF0LA")


class Search(Certificate):
    def lemma(self, statement, proof):
        # Only the Word rewrite and its cost are needed here.
        return None


rules = Search()


def runs(parts):
    result = []
    for bit, size in parts:
        if size == 0:
            continue
        assert size > 0
        if result and result[-1][0] == bit:
            size += result.pop()[1]
        result.append((bit, size))
    if result and result[-1][0] == 0:
        result.pop()
    return tuple(result)


def push(bit, size, tape):
    return runs(((bit, size),) + tape)


def drop(tape, size):
    while tape and size >= tape[0][1]:
        size -= tape[0][1]
        tape = tape[1:]
    if size and tape:
        return ((tape[0][0], tape[0][1]-size),) + tape[1:]
    return tape


def encode(word):
    parts = [run for d in word[:-1] for run in ((1, 3*d), (0, 1))]
    return runs(parts + [(1, 7+3*word[-1])])


def decode(tape):
    digits = []
    for bit, size in tape:
        if bit:
            if size >= 7 and size % 3 == 1:
                return tuple(digits) + ((size-7)//3,)
            if size % 3 or size > 1500:
                break
            digits.append(size//3)
        else:
            if size > 5:
                break
            digits.extend([0]*(size-int(bool(digits))))
    return None


@cache
def phase(word):
    """Uninterrupted blank-exterior phase and a bound on its rightward reach.

    A single pass of cost c+15 stays within c+15 cells of its starting
    head. The next pass starts three cells farther right. Framing a digit d
    adds 14*d+4 to each individual pass cost.
    """
    end = word
    passes = cost = reach = 0
    parts = []
    if len(word) > 1 and word[0]:
        suffix, passes, cost, reach, _ = phase(word[1:])
        if passes:
            d = word[0]
            end = (d,) + suffix
            cost += passes*(14*d+4)
            reach += 14*d+4
            parts.append(("frame", word[1:], d))
    atom = rules.one(end)
    if atom:
        after, elapsed, _ = atom
        parts.append(("atom", end, 0))
        reach = max(reach, 3*passes+elapsed+15)
        passes += 1
        cost += elapsed
        end, count, elapsed, distance, _ = phase(after)
        if count:
            parts.append(("suffix", after, 0))
            reach = max(reach, 3*passes+distance)
            passes += count
            cost += elapsed
    return end, passes, cost, reach, parts


def guarded(word, clearance, extra=0):
    """Use only passes that cannot read the next exterior one."""
    end, count, cost, reach, parts = phase(word)
    if clearance is None or reach+extra <= clearance:
        return end, count, cost
    end = word
    count = cost = 0
    for kind, src, digit in parts:
        remaining = clearance - 3*count
        if kind == "frame":
            overhead = 14*digit+4
            after, n, elapsed = guarded(src, remaining, extra+overhead)
            end = (digit,) + after
            elapsed += n*overhead
            possible = phase(src)[1]
        elif kind == "atom":
            after, elapsed, _ = rules.one(src)
            if elapsed+15+extra > remaining:
                break
            end = after
            n = possible = 1
        else:
            end, n, elapsed = guarded(src, remaining, extra)
            possible = phase(src)[1]
        cost += elapsed
        count += n
        if n < possible:
            break
    return end, count, cost


def literal(left, right, state):
    bit = right[0][0] if right else 0
    op = TABLE[state][3*bit:3*bit+3]
    if op == "---":
        raise StopIteration
    write, state = int(op[0]), ord(op[2])-ord("A")
    rest = drop(right, 1)
    if op[1] == "R":
        return push(write, 1, left), rest, state, 1, 1, "literal"
    before = left[0][0] if left else 0
    return drop(left, 1), push(before, 1, push(write, 1, rest)), state, 1, -1, "literal"


def wall(left, right):
    # Entry is 0 D>10, immediately to the right of a wall of ones.
    older = left[1:]
    width = older[0][1]
    body = drop(right, 2)
    if not body or body[0][0] == 0:
        end = push(0, width+1, push(1, 4, drop(body, 1)))
        return drop(older, width+1), end, 0, width+6, -width-2, "empty wall"
    word = decode(body)
    if word:
        size = sum(n for _, n in encode(word))
        outside = drop(body, size)
        assert not outside or outside[0][0] == 0
        clearance = 2+size+outside[0][1] if outside else None
        end, count, cost = guarded(word, clearance)
        if count:
            encoded = encode(end)
            suffix = ()
            if outside:
                gap = clearance-3*count-2-sum(n for _, n in encoded)
                assert gap >= 0
                suffix = ((0, gap),) + outside[1:]
            right = runs(((1, 1), (0, 1)) + encoded + suffix)
            left = ((0, 1), (1, width+3*count)) + older[1:]
            return left, right, 3, cost+15*count, 3*count, "passes"
    if body[0] == (1, 3) and len(body) > 1 and body[1][1] >= 2:
        after = drop(body, 5)
        ones = after[0][1] if after and after[0][0] else 0
        if ones < 3000 and ones % 3 == 0:
            k = ones//3
            left = runs(((0, 1),) + ((1, 2), (0, 1))*(k+1) + ((1, 3),) + older)
            right = runs(((1, 1), (0, 1)) + drop(after, ones+1))
            return left, right, 3, 32+3*k, 6+3*k, "open digit"
        if 7 <= ones < 3000 and ones % 3 == 1:
            blocks = (ones-7)//3+4
            left = runs(((1, 2), (0, 1))*blocks + ((1, 3),) + older)
            return left, drop(after, ones), 3, 26+3*blocks, ones+7, "open tail"
    return None


def advance(left, right, state):
    if state == 3 and left[:1] == ((0, 1),) and right[:1] == ((1, 1),) and len(right) > 1:
        result = wall(left, right)
        if result:
            return result
    if state == 0:
        clear = not right or (right[0][0] == 0 and right[0][1] >= 4)
        if clear and left[:2] == ((1, 2), (0, 1)) and len(left) > 2 and left[2][1] >= 2:
            width = left[2][1]
            end = push(0, width+2, push(1, 6, drop(right, 4)))
            return drop(left, width+4), end, 0, width+20, -width-4, "older wall"
        if right[:1] == ((1, 1),) and left and left[0][0] == 1 and left[0][1] > 8:
            count = left[0][1]+1
            return drop(left, count), push(0, count+1, drop(right, 1)), 0, count, -count, "erase ones"
    return literal(left, right, state)


def search(operations):
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))
    left = right = ()
    state = moves = head = 0
    exterior = ((1, 5), (0, 1), (1, 2), (0, 1), (1, 3))
    for i in range(operations):
        if state == 0 and left == exterior and right[:2] == ((0, 1324), (1, 6)):
            print(f"restart after {moves} moves, head {head}, right runs {right[:8]}", flush=True)
        if i and i % 100000 == 0:
            phase.cache_clear()
            rules.one.cache_clear()
        try:
            left, right, state, time, displacement, _ = advance(left, right, state)
        except StopIteration:
            print(f"B1 after {moves} defined moves, head {head}, left {left}, right {right}")
            return
        moves += time
        head += displacement
    print(f"Search stopped after {moves} defined moves, head {head}, state {chr(65+state)}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operations", type=int, default=320000)
    search(parser.parse_args().operations)
