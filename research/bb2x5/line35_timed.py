"""Bit-parallel timed boundary returns for BB(2,5) line 35."""
import argparse
import base64
import hashlib
import json
import zlib
from collections import Counter
from itertools import product
from pathlib import Path
from frontiers.checkpoints import atomic_json, checksum
from prior_sweeps import TapeMachine, TERNARY_CLOSE, direct_epoch, word_sweep


HEADERS = ('2', '1', '3', '1323', '1313', '1331')
EXTRA_RIGHT = (1, 1, 2, 8, 9, 11)


def encode(word):
    masks = [0, 0]
    for symbol in word:
        for i in range(2):
            masks[i] = 2 * masks[i] + (symbol == i + 1)
    return len(word), *masks


def unpack(n, opens, closes):
    length = (n + 7) // 8
    o = opens.to_bytes(length, 'little')
    c = closes.to_bytes(length, 'little')
    return bytes(1 if o[j//8] & (1 << (j%8)) else 2 if c[j//8] & (1 << (j%8)) else 3
                 for j in reversed(range(n)))


HEADER_MASKS = tuple(encode(tuple(map(int, h))) for h in HEADERS)


def sweep(n, opens, closes):
    """For words ending in a closing. Return new boundary plus matching statistics."""
    assert n >= 1 and closes & 1
    whole = (1 << n) - 1
    cuts = (whole << 1) | 1
    guard = area = levels = cut8 = 0
    while closes:
        # Carries encode one LIFO matching level, as in line37_orbit.match.
        # Occupancy at bit j crosses the cut j cells in from the right.
        occupied = (closes + ~opens) ^ closes ^ ~opens
        finite = occupied & cuts
        area += finite.bit_count()
        guard += finite >> n
        cut8 += (finite >> max(0, n-8)) & 1
        levels += 1
        closes &= occupied
        opens &= ~occupied
    if guard >= 6:
        return None, None, guard, levels, cut8
    h, h_open, h_close = HEADER_MASKS[guard]
    left = (opens >> 1) | (int(guard < 2) << (n - 1))
    new_open = ((~(opens ^ left) & whole) << 1) | (h_open << (n + 1))
    new_close = ((opens & ~left) << 1) | 1 | (h_close << (n + 1))
    right_moves = 2*n + 1 + area - opens.bit_count() + EXTRA_RIGHT[guard]
    return (n + h + 1, new_open, new_close), 2*right_moves + h, guard, levels, cut8


def audit():
    for n in range(1, 9):
        for prefix in product((1, 2, 3), repeat=n-1):
            w = prefix + (2,)
            state, elapsed, guard, levels, cut8 = sweep(*encode(w))
            expected, _ = word_sweep(w, TERNARY_CLOSE)
            machine = TapeMachine(TERNARY_CLOSE, w, left=1)
            assert direct_epoch(machine, (1, 2, 3)) == expected
            d = maximum = 0
            for x in reversed(w):
                d = max(0, d + (x == 2) - (x == 1))
                maximum = max(maximum, d)
            assert (guard, levels, cut8) == (d, maximum, 0)
            if state is None:
                assert d >= 6 and expected is None
            else:
                assert state == encode(expected) and machine.steps == elapsed
                assert machine.head == -len(HEADERS[d])


def check_window(window, state, head, raw_time):
    machine = TapeMachine(TERNARY_CLOSE, unpack(*state), left=head+1, head=head)
    elapsed = window['steps'] - raw_time
    for _ in range(elapsed):
        assert machine.step()
    cells = zlib.decompress(base64.b64decode(window['tape_zlib_base64'], validate=True))
    expected = {window['left'] + i: x for i, x in enumerate(cells) if x}
    assert window['machine'] == TERNARY_CLOSE
    assert (machine.state, machine.head) == (window['state'], window['head'])
    assert machine.tape == expected
    print('matched full window at raw step', window['steps'], 'after', elapsed, 'literal instructions')


def load(path):
    doc = json.loads(path.read_text())
    record = doc['payload']
    if doc['sha256'] != checksum(record) or record['format'] != 'bb2x5-line35-epoch-v1':
        raise ValueError('invalid line 35 checkpoint checksum or format')
    tape = zlib.decompress(base64.b64decode(record['tape_zlib_base64'], validate=True))
    if (record['machine'] != TERNARY_CLOSE or record['state'] != 'A'
            or record['left'] != record['head'] + 1 or record['epoch'] < 5
            or record['steps'] < 97 or len(tape) != record['cells']
            or len(tape) < 5 or tape[-2:] != bytes([1, 2])
            or not set(tape) <= {1, 2, 3}):
        raise ValueError('invalid line 35 tape or epoch')
    # Construct both big integers in linear time, including at long checkpoints.
    masks = tuple(int(bytes(49 if digit == role else 48 for digit in tape), 2)
                  for role in (1, 2))
    return record, (len(tape), *masks)


def run(end, window, output, resume=None):
    if resume is None:
        machine = TapeMachine(TERNARY_CLOSE)
        for _ in range(5):
            word = direct_epoch(machine, (1, 2, 3))
        state = encode(word)
        assert machine.steps == 97 and machine.head == -5 and word == list(map(int, '213111112'))
        start, time, head = 5, machine.steps, machine.head
    else:
        record, state = load(resume)
        start, time, head = record['epoch'], record['steps'], record['head']
    if end < start or window and window['steps'] < time:
        raise ValueError('requested endpoint or window precedes the starting checkpoint')
    last = {}
    last_mismatch = None
    peak = 0
    guards = Counter()
    for epoch in range(start, end):
        new_state, elapsed, debt, levels, cut8 = sweep(*state)
        if new_state is None:
            raise RuntimeError(f'Physical halt during epoch {epoch}')
        if window and time <= window['steps'] < time + elapsed:
            check_window(window, state, head, time)
            window = None
        state = new_state
        if levels > peak:
            print('first maximum interval debt', levels, 'at epoch', epoch,flush=True)
            peak = levels
        key = epoch % 89
        phase = (debt, cut8)
        if key in last and last[key] != phase:
            last_mismatch = epoch
        last[key] = phase
        guards[debt] += 1
        time += elapsed
        head -= len(HEADERS[debt])
    tape = unpack(*state)
    print('epoch',end,'width',len(tape),'head',head,'steps',time)
    print('SHA256 of word bytes',hashlib.sha256(tape).hexdigest())
    if output:
        record = {'format': 'bb2x5-line35-epoch-v1', 'machine': TERNARY_CLOSE, 'epoch': end, 'steps': time, 'head': head,
                  'state': 'A', 'left': head + 1, 'cells': len(tape),
                  'tape_zlib_base64': base64.b64encode(zlib.compress(tape, 9)).decode()}
        atomic_json(output, {'payload': record, 'sha256': checksum(record)})
    if window:
        if window['steps'] != time:
            raise ValueError('run must reach the requested window')
        check_window(window, state, head, time)
    print('guard histogram',sorted(guards.items()),'last lag-89 guard/cut8 mismatch',last_mismatch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs',type=int,default=150000)
    parser.add_argument('--check-window', type=Path, help='cross-check a repository window JSON from blank')
    parser.add_argument('--resume', type=Path, help='start at a saved line 35 epoch')
    parser.add_argument('--output', type=Path, help='save the full endpoint as JSON')
    args = parser.parse_args()
    if not __debug__:
        parser.error('assertions must be enabled')
    if args.epochs < 5:
        parser.error('epochs must be at least 5')
    window = json.loads(args.check_window.read_text())['payload'] if args.check_window else None
    if window and window['steps'] < 97:
        parser.error('window must be at or after epoch 5')
    audit()
    run(args.epochs, window, args.output, args.resume)
