"""Check raw time, both tape halves, batch boundaries, and saved continuation."""
import base64
import itertools
import json
import os
from pathlib import Path
import unittest
import zlib

from longitudinal import (CandidateUndefined, DRIVERS, Driver, HALTED, ROOT, TapeMachine,
                          literal_group, resolve_candidate)
import survey

ENGINE = Path(os.environ.get('BB25_STREAM', '/tmp/bb25-stream'))
WINDOW = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))


def cells(driver, state):
    """Expand a small canonical boundary into an ordinary physical tape."""
    _, pieces = driver.left(driver.excursions(state['groups']))
    left = []
    for copies, blocks in pieces:
        nearest_first = [digit for block in blocks for digit in reversed(block)]
        left.extend(nearest_first * copies)
    word = list(reversed(left)) + list(map(int, state['positive_tape']))
    return {i - len(left): digit for i, digit in enumerate(word) if digit}


class LongitudinalTests(unittest.TestCase):
    def test_literal_and_negative_driver(self):
        for line in DRIVERS:
            with self.subTest(line=line):
                driver = Driver(line)
                literal = TapeMachine(driver.machine)
                state = driver.blank()
                for batch in (1, 2, 7, 17):
                    state = driver.advance(ENGINE, state, batch, 1 << 20)
                    while literal.steps < state['steps']:
                        self.assertTrue(literal.step())
                    self.assertEqual((literal.head, literal.state, literal.tape),
                                     (0, state['state'], cells(driver, state)))
                for n in (1, 23, 368, 9971):
                    cost, pieces = driver.left(n)
                    blocks = [block for count, run in pieces for _ in range(count) for block in run]
                    expected, total = [], 0
                    while n:
                        n, elapsed, word = driver.block(n)
                        expected.append(word)
                        total += elapsed
                    self.assertEqual((cost, blocks), (total, expected))

    def test_saved_frontiers_and_splits(self):
        recipes = json.loads((ROOT/'frontiers/stream-recipes.json').read_text())
        for line in DRIVERS:
            with self.subTest(line=line):
                driver = Driver(line)
                checkpoint = driver.load(ROOT/'frontiers/runs'/f'stream-{line:02}.json')
                self.assertEqual(checkpoint['groups'], sum(n*k for n,k in recipes[str(line)]))
                for start in (driver.blank(), checkpoint):
                    direct = driver.advance(ENGINE, start, 50001, 1 << 24)
                    split = driver.advance(ENGINE, start, 20000, 1 << 24)
                    split = driver.advance(ENGINE, split, 30001, 1 << 24)
                    self.assertEqual(direct, split)

    def test_literal_refinement_and_physical_halt(self):
        driver = Driver(13)
        state = driver.advance(ENGINE, driver.blank(), 10**12, 1 << 29)
        self.assertEqual(literal_group(driver, state, 100000), driver.advance(ENGINE, state, 1, 1 << 24))
        # Auxiliary tapes force concrete undefined entries and exercise the search
        # without attributing any of these halts to the blank computation.
        for line in (10, 12, 13, 21, 31):
            driver = Driver(line)
            alphabet = sorted(set(driver.machine[3*j] for j in range(5) if driver.machine[3*j].isdigit())
                              | set(driver.machine[16+3*j] for j in range(5) if driver.machine[16+3*j].isdigit()))
            for digits in itertools.product(alphabet, repeat=3):
                seed = {**driver.blank(), 'groups': 4, 'state': driver.period[-1],
                        'steps': 10000, 'positive_tape': ''.join(digits)}
                literal = TapeMachine(driver.machine)
                literal.steps, literal.state, literal.tape = seed['steps'], seed['state'], cells(driver, seed)
                finished = driver.excursions(seed['groups'])
                target = driver.excursions(seed['groups']+32)
                while finished < target and literal.steps < 200000:
                    old = literal.head
                    if not literal.step():
                        break
                    if old == -1 and literal.head == 0:
                        finished += 1
                else:
                    continue
                with self.assertRaises(CandidateUndefined):
                    driver.advance(ENGINE, seed, 32, 1 << 20)
                history = []
                end = resolve_candidate(driver, ENGINE, seed, 32, 1 << 20, 200000, history.append)
                self.assertEqual(end['format'], HALTED)
                self.assertEqual(history[-1], end)
                self.assertEqual((literal.steps, literal.head, literal.state),
                                 (end['steps'], end['head'], end['state']))
                positive = {i: n for i, n in literal.tape.items() if i >= 0}
                self.assertEqual(positive, {i:int(v) for i,v in enumerate(end['positive_tape']) if v != '0'})
                break
            else:
                self.fail(f'no auxiliary halt reached on line {line}')

    def test_full_tapes_meet_independent_long_checkpoints(self):
        for line in DRIVERS:
            with self.subTest(line=line):
                driver = Driver(line)
                reference = survey.load(ROOT/'frontiers/runs'/f'window-{line:02}.json', line, driver.machine)
                left, right = 0, 100000
                last = driver.blank()
                while right-left > 1:
                    mid = (right+left)//2
                    state = driver.advance(ENGINE, driver.blank(), mid, 1 << 24)
                    if state['steps'] > reference['steps']:
                        right = mid
                    else:
                        left, last = mid, state
                self.assertLess(reference['steps']-last['steps'], 10**7)
                tape = cells(driver, last)
                origin = min(tape)
                physical = bytes(tape.get(pos, 0) for pos in range(origin, max(tape)+1))
                seed = {**reference, 'steps':last['steps'], 'head':0, 'state':last['state'],
                        'left':origin, 'cells':len(physical),
                        'tape_zlib_base64':base64.b64encode(zlib.compress(physical, 9)).decode()}
                got, _ = survey.advance(WINDOW, line, driver.machine, seed, reference['steps'], 10**8, 7)
                self.assertEqual(got, reference)


if __name__ == '__main__':
    unittest.main()
