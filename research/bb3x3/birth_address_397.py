"""Verify the extension code and finite odometer addresses in BIRTH_ADDRESS_397.md."""
from functools import cache

from check_bb33 import H397, sweep
from regular_guard_397 import RETURN
from transitive_section_397 import propagate

A, B, C, D, E, F = range(6)
INVERSE = tuple(tuple(next((bit, successor) for bit, (out, successor) in enumerate(row)
                           if out == desired) for desired in (0, 1)) for row in H397.rules)
BIRTH_BITS = {A: (0,), B: (1, 1), D: (0, 0, 0), F: (1, 1, 1, 1)}


def column(sequence, bit, rules):
    section = []
    for mode in sequence:
        bit, mode = rules[mode][bit]
        if mode != -1:
            section.append(mode)
    return bit, tuple(section)


def act(sequence, bits, rules):
    result = []
    for bit in bits:
        bit, sequence = column(sequence, bit, rules)
        result.append(bit)
    return tuple(result), sequence


def birth(state, mode):
    prefix, future = act(state, BIRTH_BITS[mode], INVERSE)
    if mode in (A, D):
        future = (C,) + future
    return prefix, future


def births(state, modes):
    prefix = ()
    for mode in modes:
        additional, state = birth(state, mode)
        prefix += additional
    return prefix, state


def digits(bits):
    return ''.join(map(str, bits))


def check_equations():
    for mode, prefix in BIRTH_BITS.items():
        new_bits, continuation = act((mode,), prefix, H397.rules)
        assert new_bits == H397.extension[mode]
        assert continuation == ((C,) if mode in (A, D) else ())
    assert act((C,), (0, 0), H397.rules) == ((1, 1), (C,))
    # Check both identities on arbitrary unknown tails by comparing their sections.
    assert births((), (A, B)) == births((), (D,))
    assert births((), (B, B)) == births((), (F,))

    # On either constant ray each carry and inverse carry is eventually constant.
    for rules in (H397.rules, INVERSE):
        for bit in (0, 1):
            for initial in range(6):
                mode, outputs, seen = initial, [], {}
                while mode != -1 and mode not in seen:
                    seen[mode] = len(outputs)
                    output, mode = rules[mode][bit]
                    outputs.append(output)
                if mode != -1:
                    assert len(set(outputs[seen[mode]:])) == 1


def check_paired_code():
    states = ((), (C,), (C, F), (C, E), (C, B))
    rows = (
        ('11', 0, '00010011', 1),
        ('00', 1, '10001011', 2),
        ('00', 3, '11101011', 2),
        ('01', 4, '10010011', 2),
        ('10', 1, '00001011', 2),
    )
    for state, (short, short_state, long, long_state) in zip(states, rows):
        assert births(state, (B,)) == (tuple(map(int, short)), states[short_state])
        assert births(state, (D, D, B)) == (tuple(map(int, long)), states[long_state])
        assert short[0] != long[0]


@cache
def byte_action(sequence, byte):
    """Map eight occupied bits and return their outgoing chronological word."""
    output = 0
    for index in range(8):
        bit, sequence = column(sequence, (byte >> index) & 1, H397.rules)
        output |= bit << index
    return output, sequence


def fixed_return(word, width):
    output, sequence = 0, RETURN
    for index in range(0, width, 8):
        byte, sequence = byte_action(sequence, (word >> index) & 255)
        output |= byte << index
    return output & ((1 << width) - 1)


def main():
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    check_equations()
    check_paired_code()
    physical, state, padding, history = (), (), (), []
    for _ in range(128):
        for source in RETURN:
            changed = list(physical)
            edge = propagate(changed, source)
            physical = sweep(H397, physical, source)
            assert physical is not None
            if edge != -1:
                history.append(edge)
                extra, state = birth(state, edge)
                padding += extra
            assert len(physical) == len(padding)

    # Replay on the fixed initial padding and compare at every microstep.
    fixed, dynamic = list(padding), ()
    for _ in range(128):
        for source in RETURN:
            propagate(fixed, source)
            dynamic = sweep(H397, dynamic, source)
            assert tuple(fixed[:len(dynamic)]) == dynamic
    print("First 128 returns, growing edge labels:", ''.join('abcdef'[m] for m in history))
    print("Forced initial padding:", digits(padding))

    # Verify an actual additive address by direct enumeration of the finite orbit.
    width = 20
    target = sum(bit << index for index, bit in enumerate(padding[:width]))
    word = 0
    for address in range(1 << width):
        if word == target:
            break
        word = fixed_return(word, width)
    else:
        raise AssertionError("Target outside the fixed-width orbit.")
    assert address == 682853
    word = target
    for _ in range(128):
        word = fixed_return(word, width)
    assert word == sum(bit << i for i, bit in enumerate(dynamic[:width]))
    print(f"Forced normalized address modulo 2^{width}: {address}")


if __name__ == "__main__":
    main()
