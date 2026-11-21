"""Exact Fibonacci-reset observations and unbounded countercertificates.

Uses the accompanying Wily research modules (standard library only).
The blank-machine question remains undecided.
"""
from certificates import pass_word
from c_safety import c_nonhalting
from return_sections import prefix_action, reduce_word, return_section, section


def fibonacci_weights(n):
    values = [1, 2]
    while len(values) < n:
        values.append(values[-1] + values[-2])
    return values[:n]


def fibonacci_value(word):
    return sum(weight * int(bit) for weight, bit in
               zip(fibonacci_weights(len(word)), word))


def reset_code(n):
    """Canonical Zeckendorf digits (LSB first), followed by exactly two zeros."""
    if n == 0:
        return '0'
    assert n > 0
    weights = [1, 2]
    while weights[-1] <= n:
        weights.append(weights[-1] + weights[-2])
    weights.pop()
    digits = ['0'] * len(weights)
    for index in reversed(range(len(weights))):
        if weights[index] <= n:
            digits[index] = '1'
            n -= weights[index]
    assert n == 0 and '11' not in ''.join(digits)
    return ''.join(digits) + '00'


def halt_certificate(exponent, calls):
    word = reset_code(5 ** exponent)
    start = word
    for call in range(calls - 1):
        word = pass_word(word)
        assert word is not None
    last = word
    assert pass_word(word) is None
    return {'exponent': exponent, 'start': start, 'last_word': last,
            'halts_on_call': calls}


def nonhalting_certificate(exponent, expected_period):
    """Returns an exact infinite-family section certificate plus empty base.

    The section reduction is justified on nonempty tails only. We therefore
    check the empty-tail initial cycle independently and enter a nonempty
    c-safe tail before applying the unbounded closure theorem.
    """
    prefix = reset_code(5 ** exponent)
    period, section = return_section(prefix)
    assert period == expected_period and section == (2, 2, 2)
    current_prefix, raw_sections = prefix, []
    actual = prefix
    for _ in range(period):
        current_prefix, mode = prefix_action(current_prefix)
        raw_sections.append(mode)
        actual = pass_word(actual)
        assert actual is not None
    assert current_prefix == prefix
    assert reduce_word(raw_sections) == (2, 2, 2)
    assert actual.startswith(prefix)
    tail = actual[len(prefix):]
    assert tail == '110100' and c_nonhalting(tail)
    return {'exponent': exponent, 'prefix': prefix, 'period': period,
            'section': 'ccc', 'first_cycle_tail': tail,
            'tail_is_nonempty_and_c_safe': True,
            'conclusion': 'nonhalting for this seed; not the blank seed'}


def orbit_separation():
    small = reset_code(5 ** 5)
    target = reset_code(5 ** 8)[:len(small)]
    period, _ = return_section(small)
    assert period == 2048
    prefix = small
    for _ in range(period):
        assert prefix != target
        prefix, _ = prefix_action(prefix)
    assert prefix == small
    return {'target_prefix_length': len(small), 'cycle_period': period,
            'conclusion': 'No a-iterate of R(5^8) can start with R(5^5)'}



def mixed_section_certificate():
    prefix = reset_code(5 ** 8)
    period, mixed = return_section(prefix)
    assert period == 8192
    assert ''.join('abcde'[q] for q in mixed) == 'cccacbbbbabbcabcbabc'
    actual = prefix
    for _ in range(period):
        actual = pass_word(actual)
        assert actual is not None
    assert actual == prefix + '00011010001100'

    def cycle_counts(word, depth):
        from collections import Counter
        nodes = [(1, word)]
        for _ in range(depth):
            new_nodes = []
            for length, ret in nodes:
                bit, left = section(ret, 0)
                _, right = section(ret, 1)
                if bit == 0:
                    new_nodes.extend(((length, left), (length, right)))
                else:
                    new_nodes.append((2 * length, reduce_word(left + right)))
            nodes = new_nodes
        return dict(Counter(length for length, _ in nodes))

    mixed_profile = cycle_counts(mixed, 5)
    cb_profile = cycle_counts((1, 2), 5)
    assert mixed_profile == {8: 3, 4: 2}
    assert cb_profile == {16: 1, 4: 4}
    return {'prefix': prefix, 'period': period,
            'temporal_section': 'cccacbbbbabbcabcbabc',
            'first_cycle_tail': '00011010001100',
            'mixed_depth5_cycle_profile': mixed_profile,
            'c_after_b_depth5_cycle_profile': cb_profile}

def verify():
    first_repair = '10100101010100010010101000100'
    assert reset_code(5 ** 8) == first_repair
    assert fibonacci_value(first_repair) == 390625
    actual = '001100'
    for index in range(583):
        actual = pass_word(actual)
        assert actual is not None
    assert actual == first_repair
    return {
        'status': 'verified; blank orbit still undecided',
        'first_repair': {'index_after_passes': 583, 'word': first_repair,
                         'fibonacci_value': 5 ** 8},
        'halting_power_seeds': [halt_certificate(2, 7),
                               halt_certificate(5, 4528)],
        'nonhalting_power_seeds': [nonhalting_certificate(11, 8192),
                                  nonhalting_certificate(14, 65536)],
        'literal_power_recurrence_obstruction': orbit_separation(),
        'mixed_section_certificate': mixed_section_certificate(),
    }


if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2))
