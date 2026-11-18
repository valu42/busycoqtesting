"""Check the seven-cell driver, its clock, and the controlled halting witness."""
import base64
import itertools
import os
from pathlib import Path
import unittest
import zlib

from check_line15_obstruction import forced_counts, verify
from check_line15_fifth import verify as fifth_language
from checkpoints import ROOT
from line15 import (Guard, Left, MACHINE, PhysicalEvent, advance,
                    physical, transfer)
from prior_sweeps import TapeMachine

ENGINE = Path(os.environ.get('BB25_LINE15', '/tmp/bb25-line15'))


class Line15Tests(unittest.TestCase):
    def test_startup_and_mature_closure(self):
        for word, digits, raw in [('ABBBA', '2221222', 73), ('AAABB', '2122222', 91)]:
            self.assertEqual(transfer(bytes(7), word), (bytes(map(int, digits)), 'AAAB', raw))
        fringe, child, cost = transfer(bytes(7), 'AAAB')
        self.assertEqual((list(fringe), child), ([2, 2, 1, 0, 1, 1, 1], ''))
        self.assertEqual(transfer(fringe, 'B'), (bytes([2, 1, 2, 2, 2, 2, 2]), 'AAAB', 91-cost))
        for digits in itertools.product((1, 2), repeat=7):
            for q in 'AB':
                word, out, _ = transfer(digits, q)
                self.assertLessEqual(set(word), {1, 2})
                self.assertLessEqual(set(out), set('AB'))
        with self.assertRaises(Guard):
            transfer(bytes(7), 'AAB')
        self.assertEqual(transfer(bytes(7), 'AAABBBABABAAB')[1], 'AAABA')

    def test_raw_and_split(self):
        driver = Left()
        tape, right = advance(driver, None, 0, 11, bytes(), 10000, 0)
        left, pieces = driver.left(driver.excursions(11))
        neg = [w[0] for copies, cycle in pieces for _ in range(copies) for w in cycle]
        machine = TapeMachine(MACHINE)
        for _ in range(left+right):
            self.assertTrue(machine.step())
        expected = {i-len(neg): s for i, s in enumerate(neg[::-1] + list(tape)) if s}
        self.assertEqual((machine.head, machine.state, machine.tape), (0, driver.period[-1], expected))
        self.assertEqual(advance(driver, ENGINE, 0, 11, bytes(), 10000, 0), (tape, right))
        first, cost = advance(driver, ENGINE, 0, 3, bytes(), 10000, 0)
        second, remaining = advance(driver, ENGINE, 3, 11, first, 10000, cost)
        self.assertEqual((second, cost + remaining), (tape, right))

    def test_physical_events(self):
        driver = Left()
        # At a period boundary the next entry is B. On these auxiliary tapes
        # the actual result is respectively a B return and a B4 halt.
        neg = driver.left(driver.excursions(1))[0]
        for data, x, elapsed, event in [([0], -1, 1, 'B return to negative half'),
                                         ([2, 0], 0, 2, 'halt')]:
            with self.assertRaises(PhysicalEvent) as found:
                physical(driver, 1, 2, bytes(data), 1000, 70)
            state = found.exception.state
            self.assertEqual((state['event'], state['head'], state['state'], state['steps']),
                             (event, x, 'B', neg + 70 + elapsed))
            word = zlib.decompress(base64.b64decode(state['positive_zlib_base64']))
            self.assertEqual(word[0], 1 if x == -1 else 4)

    def test_fifth_letter_language_and_anchors(self):
        graph = fifth_language()
        self.assertEqual(graph['root', 1][3], ('BABA', 'B'))
        self.assertEqual(graph['root', 2][3], ('BABAABB', 'B'))
        for name, depth, states, limit, bad in [
                ('root', 1, 27, 21, 'AAAAB'), ('root', 2, 833, 253, 'AABBABBABB'),
                ('interior', 1, 26, 22, 'BABABAAB'), ('interior', 2, 834, 254, 'AABBB')]:
            reached, bound, shortest, _ = graph[name, depth]
            self.assertEqual((reached, bound, shortest['A']), (states, limit, bad))
        for path in [
            ('AAABBABBAB', 'AAABBABBA', 'AAABBA'),
            ('AAABBABBABBAB', 'AAABBABBABBA', 'AAABBABBA', 'AAABBA'),
            ('AAABBABBABABBA', 'AAABBABBAA'),
            ('AAABBABBABABBAB', 'AAABBABBAAAB', 'AAABBABA'),
            ('AAABBABBABBABAABAABAB', 'AAABBABBABBAA'),
        ]:
            for parent, child in zip(path, path[1:]):
                self.assertEqual(transfer(bytes(7), parent)[1], child)

    def test_control_lengths_and_saved_fringe(self):
        for n in range(7):
            for digits in itertools.product((1, 2), repeat=n):
                for w in ('A', 'B', 'ABB', 'BAA'):
                    s = w
                    for d in reversed(digits):
                        letters = []
                        for desired in s:
                            calls = ('A' if d == 2 else '') + ('B' if desired == 'A' else 'A')
                            letters.append(calls)
                            d = 1 if desired == 'A' else 2
                        s = ''.join(letters)
                    self.assertEqual(forced_counts(digits, w), (s.count('A'), s.count('B')))
        proof = verify(ROOT/'frontiers/runs/line15-strips.json')
        self.assertEqual((proof['blank_steps'], proof['fringe_at'], proof['fringe_steps'],
                          proof['controlled_halt_at'], proof['constructed_root_calls_bits'],
                          proof['constructed_first_entry'], proof['actual_next_entry']),
                         (344289925484, 518087, 121, 518092, 259048, 'A', 'B'))


if __name__ == '__main__':
    unittest.main()
