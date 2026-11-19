#!/usr/bin/env python3
"""Verify both exact regular halting languages in TARGET_WINDOW_397.md."""
from collections import deque

from check_bb33 import H397, compressed_sweeps
from transitive_section_397 import propagate


START, END = 1_161_058, 1_162_182
D, E = 3, 4
PULSE = tuple(enumerate((D, E, D, E, D)))


def pass_cell(stream, bit):
    output = []
    for timestamp, mode in stream:
        bit, outgoing = H397.rules[mode][bit]
        if outgoing != -1:
            output.append((timestamp, outgoing))
    return tuple(output)


def boundary_trace(stream):
    """Handle every event reaching an initially empty edge in time order."""
    bits = []
    trace = []
    for timestamp, mode in stream:
        outgoing = propagate(bits, mode)
        if outgoing == -1:
            continue
        trace.append((timestamp, outgoing))
        extension = H397.extension[outgoing]
        if extension is None:
            break
        bits.extend(extension)
    return tuple(trace)


def productive_transitions(transitions, accepting):
    """Keep only reachable states that have an accepting continuation."""
    productive = set(accepting)
    while True:
        previous = len(productive)
        productive.update(s for s, children in transitions.items()
                          if any(child in productive for child in children))
        if len(productive) == previous:
            break
    return {(s, bit): child for s in productive
            for bit, child in enumerate(transitions[s]) if child in productive}


def check_languages():
    queue = deque([PULSE])
    transitions = {}
    while queue:
        s = queue.popleft()
        if s in transitions:
            continue
        transitions[s] = tuple(pass_cell(s, bit) for bit in (0, 1))
        queue.extend(transitions[s])
    assert len(transitions) == 399
    traces = {s: boundary_trace(s) for s in transitions}
    halting = {s for s, trace in traces.items()
               if trace and H397.extension[trace[-1][1]] is None}
    after_one = transitions[PULSE][1]
    after_zero = transitions[PULSE][0]
    after_zero_one = transitions[after_zero][1]

    # Any halt within five pulses, given a fixed last 001.
    capped_accepting = {s for s in transitions
                        if transitions[transitions[transitions[s][0]][0]][1] in halting}
    assert capped_accepting == {after_one}
    assert productive_transitions(transitions, capped_accepting) == {
        (PULSE, 1): after_one, (after_one, 0): PULSE,
    }

    # Drop the cap restriction and require a d growth on the first pulse.
    first_d = {s for s in halting if traces[s][0] == (0, D)}
    assert first_d == {after_zero_one}
    assert productive_transitions(transitions, first_d) == {
        (PULSE, 1): after_one, (after_one, 0): PULSE,
        (PULSE, 0): after_zero, (after_zero, 1): after_zero_one,
    }
    assert tuple(h for _, h in after_zero_one) == (D, 1, 0, 2, D)
    assert traces[after_zero_one] == ((0, D), (4, E))


def check_window():
    blank = compressed_sweeps(H397, START)
    prefix = list(blank[:40])
    assert len(blank) == 93
    assert ''.join(map(str, prefix)) == '1100010001000000000110000001100000011010'
    arrivals = []
    for t in range(START, END + 1):
        outgoing = propagate(prefix, H397.modes[t % 4])
        if outgoing != -1:
            arrivals.append((t, outgoing))
    assert arrivals == [(START, D), (1_161_153, E), (1_161_642, D),
                        (1_161_985, E), (END, D)]
    tail = blank[40:]
    assert len(tail) == 53  # Every tail in the target family has even length.
    assert compressed_sweeps(H397, START + 1024 * (1 << 11))[:40] == blank[:40]
    print('The 40-bit blank prefix transmits d,e,d,e,d over 1,124 sweeps.')
    print('The witnessed 93-bit original suffix lies outside the target.')


if __name__ == '__main__':
    check_window()
    check_languages()
    print('399 reachable streams reduce to two productive states for the 001-capped test.')
