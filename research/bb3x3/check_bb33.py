#!/usr/bin/env python3
"""Reproduce the finite checks in RANKINGS.md with Python 3.10+ (standard library).

    python3 check_bb33.py           # small independent cross-checks
    python3 check_bb33.py --full    # also reproduce the two long runs and the wall

The mathematical input is the published BB33 reduction at
https://github.com/google-deepmind/cryptids/tree/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33
and Ligocki's unshifted Bigfoot coordinates at
https://www.sligocki.com/2023/10/16/bb-3-3-is-hard.html .
Run without Python's -O option so the consistency checks execute.
"""
import argparse
import hashlib
from array import array
from bisect import bisect_right
from collections import deque
from dataclasses import dataclass


MACHINES = {
    153: "1RB0LB0RC_2LC2LA1RA_1RA1LC---",
    397: "1RB1LB2LC_1LA2RB1RB_---0LA2LA",
    531: "1RB2LA1LA_2LA0RA2RC_---0LC2RA",
    532: "1RB2LA1LA_2LA0RA2RC_---1RB2RA",
    758: "1RB2LC1RC_2LC---2RB_2LA0LB0RA",
    829: "1RB2RA1LC_2LC1RB2RB_---2LA1LA",
}


class Tape:
    """Literal full-tape interpreter, storing only nonzero symbols."""
    def __init__(self, machine_id):
        self.table = {}
        for state, row in enumerate(MACHINES[machine_id].split("_")):
            for symbol in range(3):
                rule = row[3 * symbol:3 * symbol + 3]
                if rule != "---":
                    self.table[state, symbol] = (
                        int(rule[0]), 1 if rule[1] == "R" else -1, "ABC".index(rule[2])
                    )
        self.state = self.head = self.steps = 0
        self.cells = {}

    def step(self):
        key = self.state, self.cells.get(self.head, 0)
        write, direction, self.state = self.table[key]
        if write:
            self.cells[self.head] = write
        else:
            self.cells.pop(self.head, None)
        self.head += direction
        self.steps += 1

    def run_to(self, steps):
        assert steps >= self.steps
        for _ in range(steps - self.steps):
            self.step()


# One table row per carry, indexed by the cell's old bit. Each entry is
# (new bit, outgoing carry). Bit 0 denotes tape symbol 2, bit 1 denotes symbol 1.
# Outgoing carry -1 ends a successful sweep early and leaves the rest unchanged.
@dataclass(frozen=True)
class PassModel:
    rules: tuple
    extension: tuple
    seed: tuple
    prefix: tuple
    modes: tuple


WILY = PassModel(
    rules=(((1, 1), (0, 2)), ((1, 3), (0, 0)), ((0, 2), (1, 1)), ((1, -1), (0, -1))),
    extension=((0,), None, (1, 1, 0, 0), (0, 0)),
    seed=(0, 0), prefix=(0, 1), modes=(0, 1),
)
H397 = PassModel(
    rules=(((1, 2), (0, 1)), ((1, -1), (0, -1)), ((1, 0), (0, 3)),
           ((0, 4), (1, 5)), ((0, 0), (1, 3)), ((0, 3), (1, 0))),
    extension=((1,), (0, 1), None, (0, 0, 1), None, (1, 0, 0, 1)),
    seed=(1,), prefix=(0, 1, 0, 0), modes=(0, 2, 3, 4),
)


def sweep(model, word, mode):
    """One literal pass over the supplied suffix, without prepending the new bit."""
    result = list(word)
    for index, old_bit in enumerate(word):
        result[index], mode = model.rules[mode][old_bit]
        if mode == -1:
            return tuple(result)
    extension = model.extension[mode]
    return None if extension is None else tuple(result) + extension


class EventStream:
    """A finite ordered stream of carries, stored as shared binary concatenations."""
    def __init__(self, num_modes):
        self.num_modes = num_modes
        # ID 0 is empty. IDs 1..num_modes each stand for one input carry.
        self.left = array("I", [0]) * (num_modes + 1)
        self.right = self.left[:]
        self.index = {}

    def join(self, left, right):
        if left == 0 or right == 0:
            return left or right
        # Pack two unsigned 32-bit child indices without collision.
        key = (left << 32) | right
        node = self.index.get(key)
        if node is None:
            node = len(self.left)
            self.index[key] = node
            self.left.append(left)
            self.right.append(right)
        return node

    def periodic(self, modes, rounds):
        pattern = 0
        for mode in modes:
            pattern = self.join(pattern, mode + 1)
        repeats, extra = divmod(rounds, len(modes))
        root = 0
        while repeats:
            if repeats % 2:
                root = self.join(root, pattern)
            repeats //= 2
            if repeats:
                pattern = self.join(pattern, pattern)
        for mode in modes[:extra]:
            root = self.join(root, mode + 1)
        return root

    def pop_first(self, node):
        if node <= self.num_modes:
            assert node > 0
            return node - 1, 0
        mode, rest = self.pop_first(self.left[node])
        return mode, self.join(rest, self.right[node])

    def through_cell(self, root, initial_bit, rules):
        """Evaluate (input stream, starting bit) to (final bit, output stream)."""
        output = EventStream(self.num_modes)
        self.index.clear()  # Only the child arrays of this column are still needed.
        memo = [array("Q", [0]) * len(self.left) for _ in range(2)]

        def visit(node, bit):
            if node == 0:
                return bit, 0
            if node <= self.num_modes:
                new_bit, carry = rules[node - 1][bit]
                return new_bit, carry + 1
            cached = memo[bit][node]
            if cached:
                encoded = cached - 1
                return encoded % 2, encoded // 2
            middle_bit, left = visit(self.left[node], bit)
            final_bit, right = visit(self.right[node], middle_bit)
            combined = output.join(left, right)
            memo[bit][node] = 1 + 2 * combined + final_bit
            return final_bit, combined

        final_bit, outgoing = visit(root, initial_bit)
        del visit  # Release the recursive closure's memo before the next column.
        return final_bit, output, outgoing


def compressed_sweeps(model, rounds):
    """Return the exact suffix after the periodic prefix, or None on a boundary halt."""
    stream = EventStream(len(model.rules))
    root = stream.periodic(model.modes, rounds)
    pending = deque(model.seed)
    suffix = []
    while root:
        if not pending:
            mode, root = stream.pop_first(root)
            extension = model.extension[mode]
            if extension is None:
                return None
            pending.extend(extension)
        bit, stream, root = stream.through_cell(root, pending.popleft(), model.rules)
        suffix.append(bit)
    return tuple(suffix) + tuple(pending)


def check_words():
    # Independently verify the protected prefix, a single pass, and the whole
    # tape after each of 96 passes on all three original transition tables.
    for machine_id, model in ((397, H397), (531, WILY), (532, WILY)):
        for index, (bit, mode) in enumerate(zip(model.prefix, model.modes)):
            following = (index + 1) % len(model.prefix)
            assert model.rules[mode][bit] == (model.prefix[following], model.modes[following])
        raw = Tape(machine_id)
        raw.run_to(1 if machine_id == 397 else 3)
        word = model.seed
        orientation = -1 if machine_id == 397 else 1
        boundary_state = 1 if machine_id == 397 else 0
        for t in range(97):
            tape = {raw.head + orientation * j: 2 - bit for j, bit in enumerate(word, 1)}
            assert raw.state == boundary_state and raw.cells == tape
            prefix = (model.prefix * (t // len(model.prefix) + 1))[:t]
            assert word == prefix + compressed_sweeps(model, t)
            if t == 96:
                break
            new_word = sweep(model, word, 0)
            assert new_word is not None
            word = (0,) + new_word
            next_head = raw.head - orientation
            previous_steps = raw.steps
            while True:
                raw.step()
                assert raw.steps < previous_steps + 100_000
                if raw.head == next_head and raw.state == boundary_state:
                    break
            assert raw.steps - previous_steps >= t + 1

    # Compare with ordinary chronological suffix evolution at non-power-of-two
    # horizons. Also exercise stopping at an empty edge with a halting carry.
    for model in (WILY, H397):
        suffix = model.seed
        for t in range(16_385):
            if t in (0, 127, 4_099, 16_384):
                assert compressed_sweeps(model, t) == suffix
            suffix = sweep(model, suffix, model.modes[t % len(model.modes)])
            assert suffix is not None
        for mode, extension in enumerate(model.extension):
            assert sweep(model, (), mode) == extension
            edge_case = PassModel(model.rules, model.extension, (), (), (mode,))
            assert compressed_sweeps(edge_case, 1) == extension


HALTING_TARGET, remainder = divmod(3**307 - 8_282_708_212, 13_959_275)
assert remainder == 0
WALL_NEAR, WALL_FAR = 3_403_055, 12_000_000


def champion_step(a, c):
    """One step of the shared #758/#153 two-counter map, or None at a halt."""
    if a <= c:
        if a % 2 == 0:
            return None if c % 2 == 0 else (1, a // 2 + c + 2)
        return (3 * a, c - a + 4) if c % 2 == 0 else (3 * a + 2, c - a + 1)
    if c % 2 == 0:
        return a - c - 1, 3 * (c // 2) + 2
    if a == c + 1:
        return None
    if c % 4 == 1:
        return a - c - 2, 3 * (c // 2) + 5
    if a == c + 2:
        return 3 * c + 8, 1
    if a == c + 3:
        return None
    return a - c - 4, 3 * (c // 2) + 8


# Using a shorter precomputed power table merely splits long batches.
POWERS_OF_THREE = tuple(3**n for n in range(400))


def first_return(c, batch=True):
    """First positive-time return from A(1,c) to a=1, or None on a halting branch."""
    a = 1
    while True:
        if batch and a <= c and a % 2 and c % 2 and c > 8 * a:
            # u=a+1 triples; the individual changes in c are 2-u, 2-3u, ...
            # u*3^k <= 2c+u suffices for all k individual updates to be legal.
            u = a + 1
            k = bisect_right(POWERS_OF_THREE, (2 * c + u) // u) - 1
            power = POWERS_OF_THREE[k]
            a, c = u * power - 1, c - u * ((power - 1) // 2) + 2 * k
        else:
            result = champion_step(a, c)
            if result is None:
                return None
            a, c = result
        if a == 1:
            return c


def check_champion():
    target = HALTING_TARGET
    for c in list(range(5_000)) + list(range(target - 150, target + 60)):
        assert first_return(c) == first_return(c, batch=False)
    for seed, count in (((0, 1), 122), ((1, 1), 126)):
        state = seed
        for _ in range(count):
            state = champion_step(*state)
        assert state == (1, 341)
    state = (1, target)
    for _ in range(306):
        state = champion_step(*state)
        assert state is not None
    assert champion_step(*state) is None

    # Verify conjugacy on every transition and equality of the full tapes at
    # the published raw join. Normalization anchors both tapes at the head.
    twin, representative = Tape(153), Tape(758)
    state_map = (2, 0, 1)  # A -> C, B -> A, C -> B
    symbol_map = (0, 2, 1)
    for q in range(3):
        for s in range(3):
            rule = twin.table.get((q, s))
            renamed = None
            if rule is not None:
                write, direction, next_q = rule
                renamed = symbol_map[write], -direction, state_map[next_q]
            assert representative.table.get((state_map[q], symbol_map[s])) == renamed

    def matches():
        if state_map[twin.state] != representative.state:
            return False
        mirrored = {twin.head - x: symbol_map[s] for x, s in twin.cells.items()}
        return mirrored == {x - representative.head: s for x, s in representative.cells.items()}

    twin.run_to(1_790_900)
    representative.run_to(1_841_607)
    assert not matches()
    twin.step()
    representative.step()
    assert matches()
    # Count only the odd/odd branch j to get a conservative blank-start clock.
    # Its published cost is 3*a^2 + 5*c + 6. All other branch costs are omitted.
    def cells_at_a(a, c):
        cells = {-a: 1}
        cells.update({i: 2 for i in range(1 - a, 1)})
        cells.update({2 * i + 1: 2 for i in range(c)})
        return cells

    for a, c in ((1, 3), (3, 5), (7, 7), (9, 15)):
        test = Tape(758)
        test.state, test.cells = 2, cells_at_a(a, c)
        test.run_to(3 * a * a + 5 * c + 6)
        a2, c2 = champion_step(a, c)
        relative = {i - test.head: value for i, value in test.cells.items()}
        assert test.state == 2 and relative == cells_at_a(a2, c2)
    a, c = 0, 1
    lower_bound = 2
    for _ in range(2**21):
        if a <= c and a % 2 and c % 2:
            lower_bound += 3 * a * a + 5 * c + 6
        a, c = champion_step(a, c)
    assert (a, c, lower_bound) == (107, 5_090_319, 1_000_010_983_141_407_650)
    print(f"#758: counting only branch j and entry gives >= {lower_bound:,} raw steps.")
    print("#758/#153: A(1,341) after 122/126 map steps. Raw join verified; offset 50,707.")
    print("#758: A(1,H) reaches the terminal branch on map call 307.", flush=True)


def check_wall():
    # known[d] means that A(1,H-d) reaches A(1,H). Trace each previously unseen
    # path to an already checked endpoint. The seed known[0] is the only assumption.
    target = HALTING_TARGET
    known = bytearray(WALL_FAR + 1)
    known[0] = 1
    for distance in range(WALL_NEAR, WALL_FAR + 1):
        path = []
        d = distance
        while not known[d]:
            path.append(d)
            successor = first_return(target - d)
            assert successor is not None and target - d < successor <= target
            d = target - successor
        for d in path:
            known[d] = 1
    assert all(memoryview(known)[WALL_NEAR:])
    # The adjacent start on the high side misses H. Its later fate is separate.
    c = target - WALL_NEAR + 1
    for _ in range(3_229):
        assert c < target
        c = first_return(c)
        assert c is not None
    assert c == target + 196
    print(f"#758: {WALL_FAR - WALL_NEAR + 1:,} consecutive starts reach H.", flush=True)


def bigfoot_step(a, b, c):
    """One unshifted Ligocki macro-step. Counter -1 marks the halting branch."""
    q, r = divmod(b, 6)
    return (a + (0, 1, -1, 0, 1, 0)[r],
            8 * q + c + (-1, -1, 3, 1, 3, 5)[r],
            (2, 3, 2, 5, 2, 3)[r])


def check_bigfoot():
    raw = Tape(829)
    raw.run_to(69)
    relative_tape = {pos - raw.head: value for pos, value in raw.cells.items()}
    assert raw.state == 0 and relative_tape == dict(zip(range(-5, 5), (1, 2, 1, 2, 1, 1, 1, 1, 1, 1)))

    def four(x):
        state = (10, 2 * x + 1, 2)
        for _ in range(4):
            state = bigfoot_step(*state)
        a, b, c = state
        assert b % 2 and c == 2
        return a - 10, (b - 1) // 2

    for r in range(81):
        change, output = four(r)
        assert four(r + 81) == (change, output + 256)
    assert four(5) == (-2, 22)

    blocks = 64
    blank = (2, 1, 2)
    for _ in range(4 * blocks):
        blank = bigfoot_step(*blank)
        assert blank[0] >= 0
    a, b, c = blank
    assert (a, b, c) == (39, 378_951_064_202_468_329_774_865_356_477_385, 2)
    print(f"Bigfoot: the blank orbit contains a block of {2 * b:,} ones after 256 map steps.")
    x = (b - 1) // 2
    losing_blocks = a // 2 + 1
    modulus = 81**losing_blocks
    lift = (-(175 * x + 502) * pow(175 * 256**blocks, -1, modulus)) % modulus
    other = (2, 2 * (lift * 81**blocks) + 1, 2)
    blank = (2, 1, 2)
    for _ in range(4 * blocks):
        assert (other[0], other[1] % 6, other[2]) == (blank[0], blank[1] % 6, blank[2])
        blank, other = bigfoot_step(*blank), bigfoot_step(*other)
    for _ in range(80):
        assert other[0] >= 0
        other = bigfoot_step(*other)
    assert other[0] == -1
    print("Bigfoot: a different seed shadows 256 blank-start residues, then halts 80 macro-steps later.")


def checkpoint(name, model, power, expected_length, expected_digest):
    rounds = 2**power
    bits = compressed_sweeps(model, rounds)
    assert bits is not None
    encoded = "".join(map(str, bits)).encode("ascii")
    digest = hashlib.sha256(encoded).hexdigest()
    assert len(bits) == expected_length and digest == expected_digest
    lower_bound = rounds * (rounds + 1) // 2
    print(f"{name}: {rounds:,} passes, >= {lower_bound:,} raw steps, "
          f"{len(bits)} suffix bits, SHA-256 {digest}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="reproduce the published-size checks")
    args = parser.parse_args()
    if not __debug__:
        parser.error("run without -O so all verification assertions execute")
    check_words()
    print("Original Wily pair and #397: full raw tapes match 96 passes each.", flush=True)
    check_champion()
    check_bigfoot()
    if args.full:
        checkpoint("Wily #531/#532", WILY, 96, 291, "2227cc873414ca1f243bc4281e0fa4f472146fffaab72223428979796be99bd1")
        checkpoint("#397", H397, 36, 167, "bf727ed273a689595c8eab11470f06a38b997b8aee6e44b9c05098edc174b976")
        check_wall()


if __name__ == "__main__":
    main()
