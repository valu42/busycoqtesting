"""Exact obstruction to full contextual auxiliary-clock summaries.

No external dependencies. This is a finite certificate of a universal
impossibility statement about the stated abstraction, not an orbit decision.
"""

IDENTITY = ((0, 0, 0), (1, 0, 0), (2, 0, 0))
CLOCK = (((0, 0, 0), (0, 1, 1), (1, 1, 0)),
         ((1, 0, 0), (2, 0, 0), (0, 1, 0)))
NEXT = ((1, 2), (3, 0), (2, 1), (4, 4), (4, 4))
OUTPUT = ((1, 0), (1, 0), (0, 1), (1, 0), (0, 1))
BOUNDARY = ('0', None, '1100', '00', '')
BAD_DFA = ((1, 2), (3, 0), (2, 1), (3, 3))


def pass_word(word):
    state, out = 0, []
    for bit in map(int, word):
        out.append(str(OUTPUT[state][bit]))
        state = NEXT[state][bit]
    tail = BOUNDARY[state]
    return None if tail is None else ''.join(out) + tail


def transformation(word):
    """Row(i,e,o) denotes the affine function 2**e * X_i + o."""
    matrix = IDENTITY
    for bit in map(int, word):
        rows = []
        for source, exponent, offset in matrix:
            new_source, extra_exponent, extra_offset = CLOCK[bit][source]
            rows.append((new_source, exponent + extra_exponent,
                         offset + (extra_offset << exponent)))
        matrix = tuple(rows)
    return matrix


def bad_transformation(word):
    result = []
    for state in range(4):
        for bit in map(int, word):
            state = BAD_DFA[state][bit]
        result.append(state)
    return tuple(result)


def signature(word):
    return (len(word), word.count('0'), word.count('1'), word[-2:],
            transformation(word), bad_transformation(word))


ACTUAL_INDEX = 7
ACTUAL_WORD = '1010010100001100'
BAD_WORD = '1010000101011000'
BAD_TRACE = (
    '1010000101011000',
    '0011100101011000',
    '1101100101011000',
    '0110100101011000',
    '1000111101011000',
    '0000100110011000',
    '1110100110011000',
    '0101011010011000',
    '1010100011111000',
    '0011000011111000',
    '1101000011111000',
    '0110000011111000',
    '1000000010010111',
    '0000000011110111',
    '1110000011110111',
    '0101110011110111',
    '1010011111110111',
    '0011111111110111',
    '1101111111110111',
    '0110111111110111',
)


def verify():
    actual = '001100'
    initial_trace = [actual]
    for _ in range(ACTUAL_INDEX):
        actual = pass_word(actual)
        assert actual is not None
        initial_trace.append(actual)
    assert actual == ACTUAL_WORD
    assert signature(ACTUAL_WORD) == signature(BAD_WORD)
    assert transformation(ACTUAL_WORD) == (
        (0, 6, 47), (0, 7, 92), (0, 6, 46))
    assert bad_transformation(ACTUAL_WORD) == (3, 3, 3, 3)
    for old, new in zip(BAD_TRACE, BAD_TRACE[1:]):
        assert pass_word(old) == new
    assert pass_word(BAD_TRACE[-1]) is None
    assert all(w.endswith(('00', '11')) for w in BAD_TRACE)
    return {
        'status': 'verified',
        'scope': 'obstruction, not a blank-orbit decision',
        'actual_index': ACTUAL_INDEX,
        'actual_word': ACTUAL_WORD,
        'bad_word': BAD_WORD,
        'same_features': {
            'length': len(actual), 'zeros': actual.count('0'),
            'ones': actual.count('1'), 'suffix_2': actual[-2:],
            'clock_transformation': transformation(actual),
            'halting_dfa_transformation': bad_transformation(actual),
        },
        'initial_trace': initial_trace,
        'bad_trace': BAD_TRACE,
        'bad_halts_on_call': 20,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2))
