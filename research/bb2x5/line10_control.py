"""Check the line-10 inverse table and finite forced edge branch histories."""
from itertools import product

MACHINE = '1RB2RB3LA4LA1LA_2LB3RA---4RA1RB'
INPUTS = {1: ('B', 'A'), 3: ('AAB', 'AAA'), 4: ('AB', 'AA')}
STACK = {'B': (1, 4), 'AB': (4,), 'AAB': (4, 4)}


def inverse(symbol, desired):
    parts = []
    for letter in desired:
        parts.append(INPUTS[symbol][letter == 'B'])
        symbol = 4 if letter == 'A' else 3
    return ''.join(parts)


def forced_input(branches):
    word = 'AAA'
    for branch in reversed(branches):
        for symbol in reversed(STACK[branch]):
            word = inverse(symbol, word)
        word = branch + word
    return word


def literal_history(inputs, suffix):
    """Use the given stream at the left boundary and literal rules elsewhere."""
    tape = list(suffix) + [3]
    edge = len(suffix)
    history = []
    pending = ''
    initializing = None
    for letter in inputs:
        pos, step, state = 0, 1, letter
        while pos >= 0:
            if pos == edge and step > 0 and initializing is None:
                pending += state
                if state == 'B':
                    history.append(pending)
                    initializing = edge
                    edge += len(STACK[pending])
                    pending = ''
            if pos == len(tape):
                tape.append(0)
            offset = 16 * (state == 'B') + 3 * tape[pos]
            rule = MACHINE[offset:offset+3]
            if rule == '---':
                assert pending == 'AAA'
                return history
            tape[pos] = int(rule[0])
            step = 1 if rule[1] == 'R' else -1
            pos += step
            if initializing is not None and pos < initializing:
                assert tape[edge] == 3
                initializing = None
            state = rule[2]
    raise AssertionError('forced prefix ended before a halt')


def main():
    count = 0
    for depth in range(5):
        for branches in product(STACK, repeat=depth):
            for suffix in ((), (3,), (1, 4)):
                inputs = forced_input(branches)
                for symbol in reversed(suffix):
                    inputs = inverse(symbol, inputs)
                start = forced_input(branches)
                assert len(inputs) == inverse_size(suffix, start.count('A'), start.count('B'), start[-1])
                assert literal_history(inputs, suffix) == list(branches)
                count += 1
    print(f'{count} prescribed edge histories halted on B2 in the literal machine.')


def inverse_size(tape, a, b, last):
    """Count inverse-stream letters for a stack, traversed right to left."""
    for symbol in reversed(tape):
        initial = {1: 0, 3: 2, 4: 1}[symbol]
        a, b = b + initial + a + 2*b - 1 - (last == 'B'), a
        last = 'B' if last == 'A' else 'A'
    return a+b



def check_rotations():
    expected = {'AAB': (1755, 52, 28337), 'ABA': (5937, 68, 101469)}
    for period, (calls, halt_position, moves) in expected.items():
        tape = [3]
        count = 0
        for call in range(calls):
            pos, state = 0, period[call % 3]
            while pos >= 0:
                if pos == len(tape):
                    tape.append(0)
                offset = 16 * (state == 'B') + 3 * tape[pos]
                rule = MACHINE[offset:offset+3]
                if rule == '---':
                    assert (call+1, pos+3, count) == (calls, halt_position, moves)
                    break
                tape[pos] = int(rule[0])
                pos += 1 if rule[1] == 'R' else -1
                state = rule[2]
                count += 1
            if pos >= 0:
                break
        else:
            raise AssertionError('shifted stream failed to halt by expected time')
        print(f'{period} rotation halts at {halt_position} on call {calls}.')


if __name__ == '__main__':
    from pathlib import Path
    import json
    import sys
    main()
    check_rotations()
    if len(sys.argv) > 1:
        checkpoint = json.loads(Path(sys.argv[1]).read_text())['payload']
        assert checkpoint['machine'] == MACHINE
        assert checkpoint['groups'] == 72_500_000_000
        assert checkpoint['positive_tape'][-1] == '4'
        size = inverse_size(tuple(map(int, checkpoint['positive_tape'][:-1])), 2, 0, 'A')
        print(f'{size} letters in the two-A forcing word at this checkpoint.')
