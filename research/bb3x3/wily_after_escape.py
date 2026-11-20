"""Verify the blank-conditional positive interval, survival interval and sharp family."""
from bisect import bisect_right
from functools import cache

from check_bb33 import WILY
from wily_dihedral import DIGITS, IDENTITY, Y, compose, invariant
from wily_edge_stream import append_run, through
from wily_integer_map import START, canonical_bucket, encode, image, inverse
from wily_orbit_sieve import CarryPeriod


WIDTH = 96
POSITIVE_STEPS = 98_303
SURVIVAL_STEPS = 120_075_937
SHADOW_DISTANCE = 121_797_128
SHADOW_LOW = 0x555455454202808208A48050


class OrbitColumn(CarryPeriod):
    def __init__(self, runs):
        super().__init__(runs)
        self.emission_ends = [offset[0] for offset in self.offsets[1:]] + [self.emitted]

    def input_slot(self, output_slot):
        """Global zero-based input slot of a specified emitted event."""
        copies, index = divmod(output_slot, self.emitted)
        i = bisect_right(self.emission_ends, index)
        offset = index - self.offsets[i][0]
        mode = self.runs[i][0]
        if mode in (0, 3):
            offset = 2 * offset + (mode == 3)
        return copies * self.ends[-1] + (self.ends[i - 1] if i else 0) + offset

    def mode_at(self, slot):
        index = slot % self.ends[-1]
        i = bisect_right(self.ends, index)
        offset = index - (self.ends[i - 1] if i else 0)
        mode = self.runs[i][0]
        return 3 - mode if mode in (0, 3) and offset % 2 else mode


def prefix_orbit(width):
    """Retain exactly the phases whose written prefix contains no adjacent ones."""
    runs = [(0, 1)]
    # Prefix value, count of arrivals before its phase, phase, normalized digit product.
    nodes = [(0, 0, 0, IDENTITY)]
    seed, period, history = START, 1, []
    for i in range(width):
        bit = seed % 2
        seed = (seed - 3 * bit) // 2
        state = OrbitColumn(runs)
        history.append(state)
        following, middle = through(runs, bit)
        if state.flips:
            second, restored = through(runs, middle)
            assert restored == bit
            for mode, count in second:
                append_run(following, mode, count)
        children = []
        for prefix, index, phase, group in nodes:
            count, changed = state.prefix(index)
            for half in range(state.flips + 1):
                digit = bit ^ changed ^ half
                if i and digit and prefix >> (i - 1):
                    continue
                label = compose(group, DIGITS[digit])
                if i == 0 and digit:
                    label = compose(Y, label)
                children.append((prefix + (digit << i), count + half * state.emitted,
                                 phase + half * period, label))
        nodes, runs = children, following
        period <<= state.flips
    return nodes, period, history, OrbitColumn(runs)


def time_of(history, slot):
    for column in reversed(history):
        slot = column.input_slot(slot)
    return slot


def digit_product(group, bits):
    for bit in bits:
        group = compose(group, DIGITS[bit])
    return group


def emitted(events, bit):
    outgoing = []
    for mode in events:
        bit, child = WILY.rules[mode][bit]
        if child != -1:
            outgoing.append(child)
    return tuple(outgoing)


def top_survives(events, root_width, require_positive):
    # Root -16 has a physical bucket four times its positive successor's
    # canonical bucket. The padding pair represents exactly that same integer.
    top = [1] * root_width
    if not require_positive and root_width == 2:
        top.extend((1, 0))
    for mode in events:
        for i, bit in enumerate(top):
            top[i], mode = WILY.rules[mode][bit]
            if mode == -1:
                break
        if require_positive:
            if mode != -1 or top[-1] == 0:
                return False
        elif mode != -1:
            extension = WILY.extension[mode]
            if extension is None:
                return False
            top.extend(extension)
    return True


@cache
def all_completions(events, group, width_mod_4, require_positive):
    pending = [(events, group, width_mod_4)]
    seen = set()
    while pending:
        stream, label, width = pending.pop()
        state = stream, label, width
        if not stream or state in seen:
            continue
        seen.add(state)
        for root in (2, 3):
            total = (width + root) % 4
            if total % 2 == 0:
                continue  # Positive entrance has residue 1 modulo three.
            with_root = digit_product(label, (1,) * root)
            padding = (1, 0, 1)[:(-total) % 4]
            if digit_product(with_root, padding) == IDENTITY:
                if not top_survives(stream, root, require_positive):
                    return False
        for token in ((0,), (1, 0)):
            following = stream
            for bit in token:
                following = emitted(following, bit)
            pending.append((following, digit_product(label, token), (width + len(token)) % 4))
    return True


def check_horizons():
    nodes, period, history, column = prefix_orbit(WIDTH)
    assert (len(nodes), period) == (6796, 1 << 42)
    for prefix, index, phase, label in nodes:
        for limit, positive in ((POSITIVE_STEPS, True), (SURVIVAL_STEPS, False)):
            events = []
            slot = index
            while time_of(history, slot) - phase < limit:
                events.append(column.mode_at(slot))
                slot += 1
            stream, group, width = tuple(events), label, WIDTH % 4
            if prefix >> (WIDTH - 1):
                stream = emitted(stream, 0)
                group = digit_product(group, (0,))
                width = (width + 1) % 4
            assert all_completions(stream, group, width, positive)
    return nodes, period, history, column


def check_sharpness(nodes, period, history, column):
    phase = period - SHADOW_DISTANCE
    (prefix, index, _, label), = [node for node in nodes if node[2] == phase]
    assert prefix == SHADOW_LOW and label == Y and prefix >> 95 == 0
    slots = [(time_of(history, index + i) - phase, column.mode_at(index + i))
             for i in range(4)]
    assert slots == [(119_977_633, 1), (120_075_937, 0),
                     (120_076_522, 1), (4_151_058_666, 1)]
    assert image(-2) == -1
    # s1 on T changes its numerator from -1 to -2. Thus the three high
    # arrivals 1,0,1 change -1 to -2,-1,-2, exactly the high part of START.
    assert WILY.rules[1][1] == (0, 0) and WILY.rules[0][0] == (1, 1)
    assert START == 3 * ((START * pow(3, -1, 1 << WIDTH)) % (1 << WIDTH)) - (2 << WIDTH)
    assert 3 * prefix - (1 << WIDTH) == -3_627_667_079_787_141_984_845_584

    pair = (1, 0)
    events = (1, 0)
    assert emitted(emitted(events, 1), 0) == events
    assert emitted(emitted(events, 0), 0) == (1,)
    assert top_survives((), 3, False) and not top_survives((1,), 3, False)
    low = tuple((prefix >> i) & 1 for i in range(WIDTH))
    reverse = tuple(tuple(next((old, child) for old, (written, child) in enumerate(row)
                               if written == wanted) for wanted in (0, 1)) for row in WILY.rules)
    mode = 0
    for bit in low:
        _, mode = reverse[mode][bit]
        assert mode != -1
    assert mode == 0 and reverse[0][1] == (0, 1) and reverse[1][0] == (1, 0)
    q = 3 * prefix - (1 << WIDTH)
    for d in range(4):
        bits = low + pair * d + (0, 0, 1, 1, 1)
        p, bucket = encode(bits)
        assert invariant(p) == IDENTITY and p % 3 == 1
        assert p == q + (53 << (WIDTH + 2 * d))
        assert inverse(p) == inverse(q) - (15 << (WIDTH + 2 * d))
        assert inverse(p) < 0 and canonical_bucket(inverse(p)) == bucket
    assert digit_product(IDENTITY, pair * 2) == IDENTITY


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("run with assertions enabled")
    check_sharpness(*check_horizons())
    print(f"Every first future positive excursion stays positive for {POSITIVE_STEPS:,} updates.")
    print(f"Both physical machines complete at least {SURVIVAL_STEPS:,} updates after entry.")
    print("Verified sharp alternate starts matching the blank at arbitrary finite precision.")
