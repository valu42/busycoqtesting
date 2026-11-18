#!/usr/bin/env python3
"""Bound the first extension and its branch decision from a certified cut-403 prefix."""
import argparse
import json

from line17_edge import ZERO, forced_output, initial, source_slot, suffix_event


def latest(prefix, target, rank):
    """Invert the minimum output rank at each digit under the supplied prefix."""
    prefixes = []
    for digit in range(403, target):
        prefixes.append(prefix)
        prefix = forced_output(initial(digit), prefix)
    for digit in reversed(range(403, target)):
        rank = source_slot(initial(digit), prefixes[digit-403], ZERO, rank)
    return rank


def suffix_bounds(count):
    if count < 4:
        raise ValueError('at least four certified equally spaced marks required')
    last = 6*count-1
    # The true stream has minimum cyclic gap four; the next three bits are zero.
    prefix = bytes(int(pos in range(5, last+1, 6)) for pos in range(1, last+4))
    deadline = latest(prefix, 424, 1)
    zero_hit, row = suffix_event(403, prefix, ZERO)
    if zero_hit != deadline:
        raise ValueError('zero continuation did not realize the upper rank bound')
    result = dict(cut=403, known_marks=list(range(5, last+1, 6)), through=len(prefix),
                  latest_plus12=deadline, zero_suffix_terminal_word=row[-13:],
                  latest_decision_slot_9=latest(prefix, 418, 9),
                  latest_decision_slot_10=latest(prefix, 418, 10))
    if count == 5:
        examples = []
        for gap in (6, 13, 17, 56):
            start = prefix + bytes(gap-4)
            at, row = suffix_event(403, start, bytes((1,))+bytes(gap-1))
            examples.append(dict(gap_after_29=gap, visits_at=at,
                                 symbol_at_minus_one=int(row[-13])))
        if {e['symbol_at_minus_one'] for e in examples} != {0, 1, 4}:
            raise ValueError('failed to realize each of the known return branches')
        result['conditional_gap_examples'] = examples
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('marks', type=int, help='number of certified consecutive marks at 5,11,17,…')
    args = parser.parse_args()
    print(json.dumps(suffix_bounds(args.marks), indent=2))
