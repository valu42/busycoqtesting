"""Meet the independent ten-billion-step line 15 run on both physical tape halves."""
import os
from pathlib import Path
import unittest

from checkpoints import ROOT
import line15
import survey

ENGINE = Path(os.environ.get('BB25_LINE15', '/tmp/bb25-line15'))
WINDOW = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))


class Line15WindowTest(unittest.TestCase):
    def test_meet_ten_billion_window(self):
        driver = line15.Left()
        groups = 5443
        entries = driver.excursions(groups)
        positive, right_cost = line15.native(ENGINE, b'', groups, entries, False)
        left_cost, pieces = driver.left(entries)
        target = left_cost + right_cost
        self.assertEqual(target, 10365581624)

        # The old snapshot lies in a long positive excursion between groups
        # 5,442 and 5,443. Advance precisely its remaining raw distance.
        old = survey.load(ROOT/'frontiers/runs/window-15.json', 15, line15.MACHINE)
        reached, _ = survey.advance(WINDOW, 15, line15.MACHINE, old, target, 100_000_000, 8)
        self.assertEqual((reached['steps'], reached['state'], reached['head']),
                         (target, driver.period[-1], 0))
        cells = survey.verify_state(reached, line15.MACHINE)

        nearest_first = bytearray()
        for copies, blocks in pieces:
            period = bytes(digit for block in blocks for digit in reversed(block))
            nearest_first.extend(period * copies)
        # Keep all implicitly blank cells at the ends out of both normal forms.
        physical = nearest_first[::-1] + positive
        canonical = physical.strip(b'\0')
        self.assertEqual(reached['left'], -len(nearest_first) + len(physical) - len(physical.lstrip(b'\0')))
        self.assertEqual(canonical, cells)


if __name__ == '__main__':
    unittest.main()
