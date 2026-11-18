"""Check raw time, both tape halves, batch boundaries, and saved continuation."""
import itertools
import json
import os
from pathlib import Path
import unittest

from longitudinal import DRIVERS, Driver, ROOT, TapeMachine
import survey

ENGINE = Path(os.environ.get('BB25_STREAM', '/tmp/bb25-stream'))
WINDOW = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))


def cells(driver, state):
    """Expand a small canonical boundary into an ordinary physical tape."""
    _, pieces = driver.left(state['groups'] * len(driver.period))
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

    def test_line13_meets_independent_window_at_100_billion(self):
        driver = Driver(13)
        state = driver.advance(ENGINE, driver.blank(), 81648, 1 << 24)
        reference = survey.load(ROOT/'frontiers/runs/window-13.json', 13, driver.machine)
        self.assertLess(state['steps'], reference['steps'])
        self.assertLess(reference['steps']-state['steps'], 10**7)
        tape = sorted(cells(driver, state).items())
        rows = ['unknown 0', driver.machine, f"{state['steps']} 0 1"]
        for _, group in itertools.groupby(enumerate(tape), lambda item: (item[1][0]-item[0], item[1][1])):
            entries = list(group)
            x, symbol = entries[0][1]
            rows.append(f'{x} {len(entries)} {symbol}')
        seed, _ = survey.pack(13, driver.machine, '\n'.join(rows))
        got, _ = survey.advance(WINDOW, 13, driver.machine, seed, reference['steps'], 10**8, 7)
        self.assertEqual(got, reference)


if __name__ == '__main__':
    unittest.main()
