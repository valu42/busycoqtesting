#!/usr/bin/env python3
"""Earliest possible +12 at cut 403 under the actual prefix and gap constraint."""
from line17_edge import DATA, LOCKED, cut53_period, initial
from marked_register import finite_event
from prior_frontier import pulse_on_tail


def earliest_visit(gap):
    # Keep one replayable input per (complete physical suffix, pending, cooldown).
    # Layers are indexed by inputs consumed, so merges preserve the first visit.
    pending = initial(403)[1]
    frontier = {(DATA[806:] + '2', pending, 0): 0}
    slot = 0
    while frontier:
        slot += 1
        candidates = (LOCKED[slot - 1],) if slot <= len(LOCKED) else (0, 1)
        following = {}
        for (word, pending, cooldown), marks in frontier.items():
            for bit in candidates:
                if bit and (pending or cooldown):
                    continue
                compound = bool(bit or pending)
                hit, new_word = pulse_on_tail(word, compound)
                witness = marks | (bit << (slot - 1))
                if hit:
                    return slot, [j + 1 for j in range(slot) if (witness >> j) & 1], new_word
                trit = '102'.index(word[0])
                state = (new_word, compound and trit != 0,
                         gap - 1 if bit else max(0, cooldown - 1))
                following.setdefault(state, witness)
        frontier = following
    raise ValueError('all admissible inputs terminated before the first right extension')



def lift_witness(period, witness):
    # Agree with one whole actual period at cut 53; freely choose its continuation.
    depth = 403 - 53
    power = 3 ** depth
    weights = (power - 1) // 2
    carry = 0
    survivors = []
    for slot, bit in enumerate(period, 1):
        if bit:
            delta, child = finite_event(slot + carry, depth)
            carry += delta
            if child is not None:
                survivors.append(child)
    assert survivors == witness[:4]
    previous = len(period)
    for required in witness[4:]:
        slot = power * required - 5 * weights - carry
        delta, child = finite_event(slot + carry, depth)
        assert slot >= previous + 4 and child == required and delta == 8 * weights
        carry += delta
        previous = slot

def main():
    period = cut53_period()
    marks = [j for j, b in enumerate(period) if b]
    gaps = [b - a for a, b in zip(marks, marks[1:] + [marks[0] + len(period)])]
    assert min(gaps) == 4 and all(initial(i) == (1, 0) for i in range(53, 403))
    print(f'cut 53: {len(marks)} marks in {len(period)} slots, minimum cyclic gap {min(gaps)}')
    for gap, expected in [(3, 61), (4, 65)]:
        slot, witness, word = earliest_visit(gap)
        assert slot == expected
        print(f'minimum gap {gap}: earliest +12 at cut-403 slot {slot}')
        print(f'  witness marks {witness}; cells -1 through 11: {word[-13:]}')
        if gap == 4:
            lift_witness(period, witness)
            print('  verified four-separated preimage after one full genuine cut-53 period')


if __name__ == '__main__':
    main()
