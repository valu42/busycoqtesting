"""Independent physical checks for the machine 35 isolated sweep and its forecasts."""

import json
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

from line35_guard_stream import ALPHABET, CLOSE, OPEN, balance, deficit
from line35_isolated_proof import checkpoint_forecast, erased_width, forecast, zero_seam
from line35_isolated_sweep import (
    Births, Epoch, blank_epoch, entry83, explain, halt_witness,
    read_checkpoint, run, save_checkpoint, sweep,
)
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch, word_sweep


def verify_one(word):
    state = Epoch.from_word(20, 17, -11, word)
    machine = TapeMachine(TERNARY_CLOSE, word, left=state.head+1, head=state.head)
    actual = direct_epoch(machine, ALPHABET)
    predicted, low = word_sweep(word, TERNARY_CLOSE)
    assert actual == predicted
    reading, _, successor = sweep(state)
    cut = reading.cut
    assert (reading.balance, reading.internal, reading.exterior) == (
        balance(word[:cut]), deficit(word[:cut]), deficit(word[cut:]))
    assert min(6, reading.guard) == -low
    witness = explain(state, reading, Births(state))
    if actual is not None:
        assert successor is not None and successor.digits() == bytes(actual)
        assert (successor.steps, successor.head) == (17+machine.steps, machine.head)
        assert all(c['absorbed_by'] is None or c['absorbed_by']['cell'] <= cut for c in witness['crossings'])
        return False
    assert successor is None
    h = halt_witness(state)
    assert h['steps'] == 17+machine.steps and (h['head'], h['state'], h['read']) == (
        machine.head, machine.state, machine.tape[machine.head])
    f = h['trigger_cell']
    assert deficit(word[:f-1]) == 5 and deficit(word[:f]) == 6
    tape = (3, 4, 3, 3) + (3,) * f + word[f:]
    expected = {state.head-3+i: q for i, q in enumerate(tape)}
    assert machine.tape == expected
    return True


def check_words():
    total = halts = 0
    for n in range(1, 10):
        for body in product(ALPHABET, repeat=n-1):
            halts += verify_one(body + (CLOSE,))
            total += 1
    for word in ((OPEN,)*5+(3,)*25+(CLOSE,)*14, (CLOSE,)*30+(OPEN, CLOSE),
                 (OPEN,)*14 + (CLOSE,)*12 + (3,)*4 + (CLOSE,)*10):
        halts += verify_one(word)
        total += 1
    print('literal comparisons', total, 'including', halts, 'complete B4 clocks and tapes')


def check_births():
    s = blank_epoch()
    ledger = Births(s)
    for _ in range(300):
        _, letter, new = sweep(s)
        ledger.record(letter, new.width)
        actual, _ = word_sweep(s.digits(), TERNARY_CLOSE)
        for pos in range(1, new.width-s.width+1):
            birth = ledger.cell(new, pos)
            assert birth['birth_epoch'] == new.number and birth['birth_digit'] == actual[pos-1]
        s = new
    print('every new fixed-index birth digit matches the scalar sweep for 300 epochs')


def replay_control(state, steps, expected_debts, final_guard, raw, trigger):
    machine = TapeMachine(TERNARY_CLOSE, state.digits(), left=1)
    start = state
    for expected in expected_debts:
        reading, _, successor = sweep(state)
        assert reading.exterior == expected
        actual = direct_epoch(machine, ALPHABET, limit=2_000_000)
        assert (actual is None) == (successor is None)
        if successor is not None:
            assert bytes(actual) == successor.digits()
        if state.number == start.number+steps-1:
            assert min(6, reading.guard) == final_guard and machine.steps == raw
            if trigger is not None:
                h = halt_witness(state)
                assert (h['trigger_cell'], h['steps'], h['head']) == (trigger, raw, machine.head)
        state = successor
    stop, report = run(start, steps, {'kind': 'altered'})
    assert report['attempted_sweeps'] == steps
    if trigger is not None:
        assert report['halt']['trigger_cell'] == trigger and report['halt']['steps'] == raw
        assert [p['cell'] for p in report['halt']['unmatched_origins']] == report['halt']['unmatched_closings']
    else:
        assert 'halt' not in report and stop.steps == raw
    print('copy control from epoch', start.number, 'exterior history', expected_debts,
          'last guard', final_guard, 'raw steps', raw, 'sixth closing', trigger)


def check_controls():
    for copies, last, guard, raw, trigger in ((2,5,4,3676,None), (3,7,6,3404,62)):
        state, _ = entry83(copies)
        replay_control(state, 5, [0,1,0,0,last], guard, raw, trigger)
    # A delayed block preserves the genuine prefix for seven sweeps, supplying
    # the same seven-unit pulse even after five ordinary ancestors exist.
    state = blank_epoch()
    while state.number < 80:
        _, _, state = sweep(state)
    word = state.digits()
    block = bytes((CLOSE,)) + bytes((OPEN,))*10
    genuine = state
    for _ in range(7):
        _, _, genuine = sweep(genuine)
    for copies, last, guard, raw, trigger in ((95,6,5,144193,None), (96,7,6,141981,1223)):
        control = Epoch.from_word(80, 0, 0, word[:-1] + block*copies + bytes((CLOSE,)))
        at_87 = control
        for _ in range(7):
            _, _, at_87 = sweep(at_87)
        assert at_87.digits()[:28] == genuine.digits()[:28]
        replay_control(control, 8, [1,0,0,0,1,0,0,last], guard, raw, trigger)


def check_forecasts():
    for mask in range(256):
        positions = [i+1 for i in range(8) if mask & (1 << i)]
        assert [erased_width(mask, d) for d in range(len(positions)+1)] == [0]+positions
    cases = 0
    # Every completion shares only the indicated prefix and permanent terminal pair.
    # The initial experimental row receives no ordinary-ancestry assumption.
    for text in ('1131123111231', '2222231', '13111121311111112', '11111111111111111111111111'):
        prefix = tuple(map(int, text))
        o = c = 0
        for q in prefix:
            o, c = 2*o + (q == OPEN), 2*c + (q == CLOSE)
        for gap in range(5):
            for tail in ((OPEN, CLOSE), (CLOSE,)):
                empty_seam = len(tail) == 1
                m = len(prefix) + gap + int(empty_seam)
                guards, _, _ = forecast(m, len(prefix), o, c, 0, 25, includes_terminal=empty_seam)
                for unknown in product(ALPHABET, repeat=gap):
                    word = prefix + unknown + tail
                    for lo, hi in guards:
                        word, low = word_sweep(word, TERNARY_CLOSE)
                        assert word is not None and lo <= -low <= hi
                        cases += 1
    print('guard forecasts on arbitrary small completions:', cases, 'successful comparisons')


def check_resume():
    with TemporaryDirectory() as tmp:
        for seed, origin in ((blank_epoch(), {'kind':'blank'}), entry83(3)):
            midway, _ = run(seed, 2, origin)
            path = Path(tmp)/'epoch.json'
            digest = save_checkpoint(path, midway, origin)
            reload, new_origin, got = read_checkpoint(path)
            assert midway == reload and digest == got
            resumed, report = run(reload, 6, new_origin, got)
            complete, other = run(seed, 8, origin)
            assert resumed == complete
            assert report.get('halt', {}).get('steps') == other.get('halt', {}).get('steps')
            if origin['kind'] != 'blank':
                assert new_origin == origin
        assert zero_seam(blank_epoch()) == 0
    print('both blank and altered checkpoints resume with the same endpoint or B4 clock')


def check_saved_forecast():
    runs = Path(__file__).parent/'frontiers'/'runs'
    path = runs/'line35-isolated.json'
    state, origin, digest = read_checkpoint(path)
    report = json.loads((runs/'line35-isolated-report.json').read_text())
    assert origin['kind'] == 'checkpoint' and digest == report['saved_boundary_sha256']
    assert state.location() == report['last_boundary']
    assert report['successful_sweeps'] == state.number - report['start']['epoch'] == 65536
    horizons = list(checkpoint_forecast(path, None, 256))
    assert [len(guards) for _, guards in horizons] == [1, 3, 50, 54]
    for i in range(54):
        reading, _, state = sweep(state)
        assert state is not None
        for _, guards in horizons:
            if i < len(guards):
                low, high = guards[i]
                assert low <= reading.guard <= high
    assert (state.number, state.steps) == (365591, 436208497795)
    print('all forecast guards match the exact run through epoch', state.number, 'at', state.steps, 'steps')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    check_words()
    check_births()
    check_controls()
    check_forecasts()
    check_resume()
    check_saved_forecast()
