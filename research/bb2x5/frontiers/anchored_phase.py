"""Anchored trigger and continuation checks for formal lines 21 and 22."""
import argparse
from functools import cache
import json
from itertools import product
from pathlib import Path
import subprocess
import sys

from longitudinal import Driver, literal_group
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mixed_and_sweeps import cell
from prior_sweeps import TapeMachine

PARENTS = {21: ('BAAAAA', 'BAAAABB', 'BAABBA', 'BAABBBB'), 22: ('BAAAAA',)}
MACHINES = {line: Driver(line).machine for line in PARENTS}


@cache
def entry(line, symbol, letter):
    new, out = cell(MACHINES[line], (symbol,), letter)
    return (None if new == 'halt' else new[0]), out


def feed(line, symbol, word):
    out = []
    for letter in word:
        symbol, sent = entry(line, symbol, letter)
        out.append(sent)
        if symbol is None:
            break
    return symbol, ''.join(out)


def future(line, tape):
    """First possible halt if future root letters are free, retaining the tape."""
    if set(tape[:-1]) - set('134') or set(tape[-1:]) - set('1234'):
        raise ValueError('expected mature data and at most one rightmost 2')
    forced = ''
    visited = set()
    x = 0
    while True:
        symbol = int(tape[x]) if x < len(tape) else 0
        if x >= len(tape):
            if forced in visited:
                return x, 'safe cycle', forced
            visited.add(forced)
        trigger = {0: 'BB', 2: 'B'}.get(symbol)
        if trigger and forced.startswith(trigger):
            return x, 'forced halt', forced
        if trigger and trigger.startswith(forced):
            return x, 'both continuations', forced
        end, forced = feed(line, symbol, forced)
        if end is None:
            raise AssertionError('unhandled literal halt')
        if line == 22 and end == 1:
            forced += 'A'
        x += 1


@cache
def a_run(k):
    """Minimal prefixes forcing k initial As from mature digit 3 on line 22."""
    if k == 1:
        return ('B', 'AB')
    return ('A' + 'B'*(2*k-1),) + tuple(
        'A' + 'B'*(2*j-1) + 'A' + w for j in range(1, k) for w in a_run(k-j)
    )


def grandparent_words():
    return tuple('A'+w for w in a_run(4)) + tuple('BAAA'+w for w in a_run(5))


def pull_back(line):
    """Minimal cylinders on which the child must receive a fatal parent prefix."""
    targets = PARENTS[line]
    witnesses = {target: [] for target in targets}
    pending = [('', 0, '')]
    while pending:
        word, state, sent = pending.pop()
        if state is None:
            continue
        forced = sent + ('A' if line == 22 and state == 1 else '')
        target = next((p for p in targets if forced.startswith(p)), None)
        if target is not None:
            witnesses[target].append(word)
        elif any(p.startswith(forced) for p in targets):
            for a in 'AB':
                after, out = entry(line, state, a)
                pending.append((word+a, after, sent+out))
    return witnesses


def literal_suffix(line, word):
    """Actual positive-half instructions until all supplied entries return or B2."""
    m = TapeMachine(MACHINES[line])
    for q in word:
        m.state, m.head = q, 0
        while m.head >= 0:
            if not m.step():
                assert m.state == 'B' and m.tape[m.head] == 2
                return m.head
    return None


def prefix_status(prefix, patterns):
    if prefix.startswith(patterns):
        return 1
    return 0 if any(p.startswith(prefix) for p in patterns) else -1


def check_cut_263():
    # The three mature 3s at cuts 263..265 put the A^4 test two images away.
    # At 264 the exact test is P4, so pull this set through mature 3 at 263.
    live = [('', 3, '')]
    hit, clear = set(), set()
    while live:
        word, state, sent = live.pop()
        verdict = prefix_status(sent+('A' if state==1 else ''), a_run(4))
        if verdict:
            (hit if verdict==1 else clear).add(word)
        else:
            for a in 'AB':
                end, out = entry(22, state, a)
                live.append((word+a, end, sent+out))
    assert (len(hit),len(clear),max(map(len,hit|clear))) == (654,747,29)
    common = 'ABAAAABAABAAAABAABAAAABAABAA'
    assert common+'A' in hit and common+'B' in clear
    assert 'BBBB' in hit and 'AA' in clear


def check_grandparents(line):
    # Traverse the product of a prefix trie and the literal one-cell transducer.
    # Compare "does its output begin BAAAAA?" against the 36 input cylinders.
    # Once both questions have fixed answers, the whole subtree is discharged.
    families = pull_back(line)
    targets = tuple(w for family in families.values() for w in family)
    if line == 22:
        assert set(targets) == set(grandparent_words())
        assert (len(targets), max(map(len, targets))) == (36, 18)
    else:
        assert [len(families[p]) for p in PARENTS[line]] == [6,12,18,48]
        assert (len(targets), max(map(len, targets))) == (84,21)
    pending = [('', 0, '')]
    nodes = 0
    while pending:
        prefix, state, sent = pending.pop()
        nodes += 1
        lhs = prefix_status(prefix, targets)
        rhs = -1 if state is None else prefix_status(sent, PARENTS[line])
        if lhs and rhs:
            assert lhs == rhs
            continue
        assert len(prefix) < 24, (prefix, state, sent)
        for a in 'AB':
            after, out = entry(line, state, a) if state is not None else (None, '')
            pending.append((prefix+a, after, sent+out))
    # A terminal prefix may promise the last A on either next input.
    for w in targets:
        assert literal_suffix(line, w+'A') == literal_suffix(line, w+'B') == 2
    for w in targets:
        sibling = w[:-1]+('A' if w[-1]=='B' else 'B')
        assert not sibling.startswith(targets)
    return nodes


def check_safe_cycle(line):
    # F((AB)^infinity) = B (AABA)^infinity. F sends that stream back.
    assert feed(line, 0, 'AB') == (3, 'BAABA')
    assert feed(line, 3, 'ABAB') == (3, 'AABA')
    assert feed(line, 0, 'BAABA') == (3, 'A')
    assert feed(line, 3, 'AABAAABA') == (3, 'BABABA')


def check_source_phase(line):
    period = 'ABAABABABAAAB'
    # At the true phase, the first output period has one extra letter.
    # The infinite stream at x=1 is precisely the rotation by one.
    rotated = period[1:] + period[:1]
    assert feed(line, 0, period) == (1, rotated + rotated[0])
    assert feed(line, 1, period) == (1, rotated[1:] + rotated[:1])
    phase, calls, site, ticks = ((8, 17, 6, 118) if line == 21 else (5, 34, 8, 251))
    machine = TapeMachine(MACHINES[line])
    for i in range(calls):
        machine.head, machine.state = 0, period[(phase+i) % len(period)]
        while machine.head >= 0:
            if not machine.step():
                assert (i+1, machine.head, machine.state, machine.tape[machine.head],
                        machine.steps) == (calls, site, 'B', 2, ticks)
                return
    raise AssertionError('expected physical halt with the rotated root source')


def check_controls():
    for line in PARENTS:
        check_safe_cycle(line)
        check_source_phase(line)
        for word in ('', 'A', 'B', 'AB', 'BB', 'BAB'):
            encoded = ''.join('ABA' if x=='A' else 'AA' for x in word)
            assert feed(line, 3, encoded) == (3, word)
        for q in range(5):
            # A successful fresh 0 or a pending 2 can be cleared silently.
            if q in (0, 2):
                assert feed(line, q, 'BA' if q==0 else 'A') == (3, '')
        assert feed(line, 4, 'A') == (3, 'B')
        assert feed(line, 4, 'BA') == (3, 'A')
        assert feed(line, 1, 'A') == (3, 'A')
        assert feed(line, 1, 'B') == (4, 'A' if line==22 else 'B')
        for w in PARENTS[line]:
            assert literal_suffix(line, w) == 1
    # At the 64-cycle line-22 checkpoint the final three digits are all 3.
    for letters in product('AB', repeat=4):
        word = ''.join(letters)
        state, sent = feed(22, 3, word)
        forced = sent + ('A' if state == 1 else '')
        assert forced.startswith('BB') == (word == 'AAAA')
        assert not 'BB'.startswith(forced) or forced == 'BB'
    for word, calls, halted, ticks in (('BBBB','BB',True,36), ('AA','A',False,16)):
        machine = TapeMachine(MACHINES[22], (3,3,3))
        received = ''
        alive = True
        for a in word:
            machine.head, machine.state = 0, a
            while machine.head >= 0:
                old = machine.head
                alive = machine.step()
                if not alive:
                    assert (machine.head, machine.state, machine.tape[machine.head]) == (3,'B',2)
                    break
                if (old,machine.head)==(2,3):
                    received += machine.state
            if not alive:
                break
        assert (received, not alive, machine.steps) == (calls, halted, ticks)


def read_report(lines):
    records, prefixes = [], []
    for row in lines:
        f = row.split()
        if f and f[0] == 'checkpoint':
            records.append((int(f[1]), int(f[3]), int(f[5]), f[7]))
        elif f and f[0].isdigit():
            assert int(f[0]) == len(prefixes)
            prefixes.append(f[1])
    return records, prefixes


def check_workers(engine, reference):
    from test_longitudinal import cells
    for line in PARENTS:
        driver = Driver(line)
        for cut, copies in ((0,100), (0,1024), (11,2), (24,1), (26,7)):
            out = subprocess.check_output([engine,str(line),str(cut),str(copies)],text=True)
            records,prefixes = read_report(out.splitlines())
            _,groups,steps,tape = records[0]
            state,history = driver.run_batch(reference,driver.blank(),groups,1<<29,18)
            assert (steps,tape,prefixes)==(state['steps'],state['positive_tape'],history)
            if groups==100:
                state=driver.blank()
                for _ in range(groups):
                    state=literal_group(driver,state,1000000)
                assert (steps,tape)==(state['steps'],state['positive_tape'])
                machine = TapeMachine(driver.machine)
                histories = {0: 'A'}
                while machine.steps < steps:
                    old = machine.head
                    assert machine.step()
                    x = machine.head
                    if x > old and x >= 0 and machine.steps < steps:
                        prefix = histories.get(x, '')
                        if len(prefix) < 18:
                            histories[x] = prefix + machine.state
                assert (machine.head, machine.state, machine.tape) == (0, 'A', cells(driver, state))
                assert prefixes == [histories[i] for i in range(len(histories))]


def report(line, path):
    records, prefixes = read_report(Path(path).read_text().splitlines())
    for copies,groups,steps,tape in records:
        assert Driver(line).left(13*groups)[0] == 52*groups*groups-21*groups+8
        x, outcome, forced = future(line,tape)
        print(f'line {line}, {copies} cycles, {groups} groups, {steps} steps, '
              f'last visited {len(tape)-1}, first possible B2 {x}, {outcome}, '
              f'forced input {forced or "empty"}')
    if prefixes:
        assert len(prefixes)==len(records[-1][3])
        assert all(not p.startswith(('BB',)+PARENTS[line]) for p in prefixes)
        if line==22:
            assert all(not p.startswith(grandparent_words()) for p in prefixes)


def check_bridge(line, old_path, phase_path, engine):
    """Replay the overlap from the previous published 200-billion-group run."""
    old = json.loads(Path(old_path).read_text())
    records, prefixes = read_report(Path(phase_path).read_text().splitlines())
    _, groups, steps, tape = records[-1]
    driver = Driver(line)
    assert old['machine'] == driver.machine == old['state']['machine']
    delta = groups - old['state']['groups']
    state, recent = driver.run_batch(Path(engine).resolve(), old['state'], delta, 1<<28, 18, 1<<36)
    assert (state['steps'], state['positive_tape']) == (steps, tape)
    before = [row['prefix'] for row in old['cuts']]
    for i, prefix in enumerate(prefixes):
        earlier = before[i] if i < len(before) else ''
        later = recent[i] if i < len(recent) else ''
        assert (earlier+later)[:18] == prefix
    print(f'line {line} agrees at {groups} groups, {steps} steps and all {len(prefixes)} cut histories')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', nargs=2, metavar=('PHASE_ENGINE','REFERENCE_ENGINE'))
    parser.add_argument('--report', nargs=2, metavar=('LINE','TRANSCRIPT'))
    parser.add_argument('--bridge', nargs=4, metavar=('LINE','OLD_JSON','PHASE_TRANSCRIPT','REFERENCE_ENGINE'))
    args=parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    check_controls()
    check_cut_263()
    for line in PARENTS:
        print(f'line {line} grandparent equivalence checked on {check_grandparents(line)} prefix-trie nodes')
    if args.workers:
        check_workers(*(str(Path(x).resolve()) for x in args.workers))
        print('both workers agree on all ten checkpoints and both 100-group physical replays')
    if args.report:
        line,path=args.report
        report(int(line),path)
    if args.bridge:
        line,old,phase,reference=args.bridge
        check_bridge(int(line),old,phase,reference)


if __name__=='__main__':
    main()
