#!/usr/bin/env python3
"""Check regular inductive invariants for the actual physical Wily return period."""
import argparse
import json
from collections import deque
from itertools import product
from pathlib import Path

from check_bb33 import WILY, sweep
from wily_physical_corrections import digits, through_bits

DRIVER = digits("222030111101130321301012")
BLANK_PREFIX = digits("10100101010100010010101000100")


def literal(word, modes=DRIVER):
    for mode in modes:
        word = sweep(WILY, word, mode)
        if word is None:
            break
    return word


def step_bit(modes, bit):
    following = []
    for mode in modes:
        bit, carry = WILY.rules[mode][bit]
        if carry != -1:
            following.append(carry)
    return bit, tuple(following)


def return_machine(modes=DRIVER):
    """Compile literal action on every finite tape, including empty-edge halts."""
    words = [modes]
    index = {modes: 0}
    arcs, ends = [], []
    for word in words:
        row = []
        for bit in (0, 1):
            output, remainder = step_bit(word, bit)
            if remainder not in index:
                index[remainder] = len(words)
                words.append(remainder)
            row.append((output, index[remainder]))
        arcs.append(tuple(row))
        ends.append(literal((), word))
    return arcs, ends


def apply(machine, word):
    arcs, ends = machine
    state, out = 0, []
    for bit in word:
        output, state = arcs[state][bit]
        out.append(output)
    return None if ends[state] is None else tuple(out) + ends[state]


def read(dfa, state, word):
    for bit in word:
        state = dfa[state][bit]
    return state


def forward_relations(machine, dfa):
    """Record every possible class transition while reading low bits first."""
    arcs, ends = machine
    states = [(0, 0, 0)]
    seen = set(states)
    predecessors = [set() for _ in dfa]
    dangerous = set()
    for mode, source, output in states:
        end = ends[mode]
        if end is None:
            dangerous.add(source)
        else:
            target = read(dfa, output, end)
            predecessors[target].add(source)
        for bit in (0, 1):
            next_bit, next_mode = arcs[mode][bit]
            child = (next_mode, dfa[source][bit], dfa[output][next_bit])
            if child not in seen:
                seen.add(child)
                states.append(child)
    return predecessors, dangerous


def backward_relations(machine, dfa):
    """Start at the high end and traverse the transducer arcs in reverse."""
    arcs, ends = machine
    incoming = [[] for _ in arcs]
    starts = []
    for mode, row in enumerate(arcs):
        for bit, (output, child) in enumerate(row):
            incoming[child].append((mode, bit, output))
        tail = ends[mode]
        output_state = -1 if tail is None else read(dfa, 0, reversed(tail))
        starts.append((mode, 0, output_state))
    predecessors = [set() for _ in dfa]
    dangerous = set()
    seen = set(starts)
    for mode, source, output in starts:
        if mode == 0:
            if output == -1:
                dangerous.add(source)
            else:
                predecessors[output].add(source)
        for parent, bit, written in incoming[mode]:
            target = -1 if output == -1 else dfa[output][written]
            child = (parent, dfa[source][bit], target)
            if child not in seen:
                seen.add(child)
                starts.append(child)
    return predecessors, dangerous


def safe_classes(machine, dfa, high_first=False):
    """Greatest union of input DFA states closed under the successful return."""
    relations = backward_relations if high_first else forward_relations
    predecessors, dangerous = relations(machine, dfa)
    queue = deque(dangerous)
    while queue:
        for source in predecessors[queue.popleft()]:
            if source not in dangerous:
                dangerous.add(source)
                queue.append(source)
    return set(range(len(dfa))) - dangerous


def minimize_dfa(rows, labels):
    classes = labels[:]
    while True:
        keys = {}
        following = []
        for i, (left, right) in enumerate(rows):
            key = (labels[i], classes[left], classes[right])
            following.append(keys.setdefault(key, len(keys)))
        if classes == following:
            break
        classes = following
    reps = {q: i for i, q in enumerate(classes)}
    minimal, outputs = [], []
    for q in range(len(reps)):
        i = reps[q]
        minimal.append(tuple(classes[s] for s in rows[i]))
        outputs.append(labels[i])
    return minimal, outputs


def preimage(machine, dfa, accepted):
    """DFA for the tapes whose next complete return lies in a given language."""
    arcs, ends = machine
    pairs = [(0, 0)]
    index = {pairs[0]: 0}
    rows, good = [], []
    for mode, state in pairs:
        row = []
        for output, next_mode in arcs[mode]:
            child = (next_mode, dfa[state][output])
            if child not in index:
                index[child] = len(pairs)
                pairs.append(child)
            row.append(index[child])
        rows.append(tuple(row))
        tail = ends[mode]
        good.append(int(tail is not None and accepted[read(dfa, state, tail)]))
    return minimize_dfa(rows, good)


def decode_word(code):
    """The most significant one is a delimiter. Lower bits are read low first."""
    assert code >= 1
    return tuple((code >> i) & 1 for i in range(code.bit_length() - 1))


def check_distinguishers(machine, path):
    families = {}
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        direction, p, q, t, horizon = line.split()
        rows.append((direction, int(p), int(q), int(t), int(horizon)))
    positive = [()]
    for _ in range(max(row[3] for row in rows)):
        word = literal(positive[-1])
        assert word is not None
        positive.append(word)
    for direction, p, q, t, horizon in rows:
        assert direction in {"low", "high"} and horizon > 0 and p != q
        first, second = decode_word(p), decode_word(q)
        accepted = positive[t] if direction == "low" else positive[t][::-1]
        assert accepted[:len(first)] == first
        other = second + accepted[len(first):]
        if direction == "high":
            other = other[::-1]
        for i in range(horizon):
            assert other is not None
            other = apply(machine, other)
        assert other is None
        edges = families.setdefault(direction, set())
        pair = tuple(sorted((p, q)))
        assert pair not in edges
        edges.add(pair)
    sizes = {}
    for direction, edges in families.items():
        vertices = {v for edge in edges for v in edge}
        n = len(vertices)
        assert len(edges) == n * (n - 1) // 2
        sizes[direction] = n
    return sizes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dfa", type=Path, help="JSON array of [zero, one] transitions, initial state 0")
    parser.add_argument("--high-first", action="store_true", help="read a proposed DFA from the high end")
    parser.add_argument("--start-round", type=int, default=0, help="test the proposed DFA at this exact blank round")
    parser.add_argument("--horizons", type=int, default=2, help="test exact survival-domain partitions through this many returns")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("run with assertions enabled")
    assert through_bits((0,), BLANK_PREFIX) == DRIVER
    machine = return_machine()
    assert len(machine[0]) == 508
    if args.dfa:
        table = json.loads(args.dfa.read_text())
        if not isinstance(table, list) or not table or any(
            not isinstance(row, list) or len(row) != 2 or
            any(type(value) is not int or not 0 <= value < len(table) for value in row)
            for row in table
        ):
            raise SystemExit("expected a nonempty complete DFA transition table")
        if args.start_round < 0:
            raise SystemExit("the starting round must be nonnegative")
        safe = safe_classes(machine, table, args.high_first)
        word = ()
        for _ in range(args.start_round):
            word = apply(machine, word)
            if word is None:
                raise SystemExit("the blank halted before or at the requested round")
        state = read(table, 0, reversed(word) if args.high_first else word)
        if state not in safe:
            raise SystemExit("The closed safe union excludes the specified blank round.")
        print("Verified blank nonhalting certificate. Accepting states:", sorted(safe))
        return
    if args.start_round or args.high_first:
        parser.error("--start-round and --high-first apply to a proposed --dfa")
    for width in range(10):
        for word in product((0, 1), repeat=width):
            assert apply(machine, word) == literal(word)
    # Positive control: mode 3 alone always succeeds on every word.
    # Negative control: the actual driver fails on the one-bit word 1.
    assert safe_classes(return_machine((3,)), [(0, 0)]) == {0}
    assert literal((1,)) is None and not safe_classes(machine, [(0, 0)])
    # A word's number of ones modulo three is independent of reading direction.
    modulo = [(0, 1), (1, 2), (2, 0)]
    assert forward_relations(machine, modulo) == backward_relations(machine, modulo)
    sizes = check_distinguishers(machine, Path(__file__).with_name("wily_driver_distinguishers.tsv"))
    print("Minimum states forced by distinguishable prefixes:", sizes)
    dfa, good = [(0, 0)], [1]
    for depth in range(1, args.horizons + 1):
        dfa, good = preimage(machine, dfa, good)
        safe = safe_classes(machine, dfa)
        print(f"{depth} returns: {len(dfa)} survival-language states, "
              f"{len(safe)} in the closed safe union, blank included: {0 in safe}")
        if 0 in safe:
            print("Verified nonhalting from blank.")
            break


if __name__ == "__main__":
    main()
