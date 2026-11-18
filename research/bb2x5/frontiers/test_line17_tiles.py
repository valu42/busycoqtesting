"""Differential checks for tiled phase composition, physical time and partial bursts."""
import os
from pathlib import Path
import subprocess
import unittest

from line17 import (ROOT, ReachesTerminal, advance_packed, advance_tiled, check_pulse_balances, literal_counts,
                    load, replay)
from prior_frontier import digits, marks_on_word

TILES = Path(os.environ.get('BB25_TILE17', '/tmp/bb25-tiles17'))
PACKED = Path(os.environ.get('BB25_PACK17', '/tmp/bb25-packed17'))


class TiledTests(unittest.TestCase):
    def test_short_words_against_literal(self):
        for register in ('03', '121202', '220302122222', '220312221222', '23' * 6):
            for epochs in (0, 19, 103):
                stream = bytes((0, 1, 0, 0)) * epochs
                result = subprocess.run([str(TILES), str(epochs), '100000', '1'],
                                        input=register, text=True, capture_output=True)
                expected = []
                data = digits(register)
                try:
                    for i, (trit, _) in enumerate(data):
                        start = trit, data[i-1][1] if i else 0
                        row = literal_counts(start, stream)
                        expected.append((*row.state, row.slots, row.calls, row.interior))
                        _, stream = marks_on_word(start, stream)
                except AssertionError:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('overlapping marked bursts', result.stderr)
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(expected, [tuple(map(int, line.split()))
                                                 for line in result.stdout.splitlines()])

    def test_balance_check_rejects_inconsistent_probe_and_move_counts(self):
        register = digits('020202')
        rows = []
        word = bytes((0, 1, 0, 0)) * 33
        for trit, _ in register:
            rows.append(literal_counts((trit, 0), word))
            _, word = marks_on_word((trit, 0), word)
        check_pulse_balances(33, register, rows)
        for field, increment in [('calls', 1), ('interior', 2), ('slots', 1)]:
            with self.subTest(field=field):
                old = getattr(rows[0], field)
                setattr(rows[0], field, old + increment)
                with self.assertRaisesRegex(ValueError, 'inconsistent pulse tallies'):
                    check_pulse_balances(33, register, rows)
                setattr(rows[0], field, old)

    def test_resumed_large_period_and_threads(self):
        start = load(ROOT/'frontiers/runs/line17-epochs.json')
        # Large enough to exercise mapped words and multiple complete tiles.
        epochs = 10**17 + 133
        expected = advance_packed(start, epochs, PACKED, 2**20, 2**30)
        for threads in (1, 3):
            self.assertEqual(advance_tiled(start, epochs, TILES, 2**30, threads), expected)

    def test_endpoint_and_refusal_controls(self):
        start = replay(0, 6)
        self.assertEqual(advance_tiled(start, 425, TILES, 10000, 2), replay(425, 6))
        with self.assertRaises(ReachesTerminal):
            advance_tiled({**start, 'register': '22' * 424}, 1, TILES, 10000, 2)
        with self.assertRaisesRegex(ValueError, 'word budget'):
            advance_tiled(start, 10**16, TILES, 16, 2)
        bad = subprocess.run([str(TILES), '1', '1024', str(2**32+1)],
                             input='12', capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)


if __name__ == '__main__':
    unittest.main()
