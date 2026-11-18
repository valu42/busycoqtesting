"""Compare line 9's cell table, blank sweeps and old moving-window checkpoint."""
from itertools import product
import unittest

import line9
import survey
from prior_sweeps import TapeMachine


class TestLine9(unittest.TestCase):
    def test_cell_words(self):
        # Supply B on every return from the right. Compare the entire outgoing
        # request sequence as well as the digit and the return state.
        words = line9.Words(10000)
        for length in range(1, 7):
            for letters in product('AB', repeat=length):
                incoming = line9.EMPTY
                for letter in letters:
                    incoming = words.join(incoming, getattr(line9, letter))
                for initial in (0, 2, 3):
                    if initial == 0 and letters[0] == 'A':
                        with self.assertRaises(line9.ExceptionalCall):
                            words.transmit(incoming, initial)
                        continue
                    digit = initial
                    emitted = line9.EMPTY
                    for state in letters:
                        while True:
                            digit, direction, state = line9.RULES[state, digit]
                            if direction == -1:
                                self.assertEqual(state, 'B')
                                break
                            emitted = words.join(emitted, getattr(line9, state))
                            state = 'B'
                    final, actual = words.transmit(incoming, initial)
                    def expand(node):
                        if node < 3:
                            return ('', 'A', 'B')[node]
                        left, right = words.nodes[node]
                        return expand(left) + expand(right)
                    self.assertEqual((final, expand(actual)), (digit, expand(emitted)))

    def compare(self, tm, p):
        while tm.steps < p['steps']:
            self.assertTrue(tm.step())
        self.assertEqual((tm.steps, tm.head, tm.state), (p['steps'], p['head'], 'A'))
        expected = dict.fromkeys(range(tm.head+2, 2), 2)
        expected[tm.head+1] = 3
        expected.update({i: int(d) for i, d in enumerate(p['suffix_at_2'], 2)})
        self.assertEqual(tm.tape, expected)

    def test_small_blank_sweeps(self):
        tm = TapeMachine(line9.MACHINE)
        start = None
        for goal in range(101):
            start = line9.advance(goal, start)
            self.compare(tm, start)
        self.assertEqual(line9.advance(100, node_limit=32), start)
        self.assertEqual(line9.advance(100), start)

    def test_split_batches(self):
        midway = line9.advance(2147)
        self.assertEqual(line9.advance(6991, midway, node_limit=1000),
                         line9.advance(6991))

    def test_ten_billion_checkpoint(self):
        old = survey.load(line9.ROOT/'frontiers/runs/window-09.json', 9, line9.MACHINE)
        cells = survey.verify_state(old, line9.MACHINE)
        tm = TapeMachine(line9.MACHINE, cells, old['head'], old['left'])
        tm.steps, tm.state = old['steps'], old['state']
        target = line9.advance(40822)
        self.assertLess(old['steps'], target['steps'])
        self.assertLess(target['steps'], old['steps'] + 1_000_000)
        self.compare(tm, target)


if __name__ == '__main__':
    unittest.main()
