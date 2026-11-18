"""Cross-check the exceptional positive returns and the original 10^10 snapshot."""
import base64
import os
from pathlib import Path
import unittest
import zlib

from longitudinal import CandidateUndefined, Driver, ROOT, TapeMachine, resolve_candidate
import survey
from test_longitudinal import cells


ENGINE = Path(os.environ.get('BB25_STREAM', '/tmp/bb25-stream'))
WINDOW = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))


class Line20Tests(unittest.TestCase):
    def test_defined_b2_is_replayed(self):
        driver = Driver(20)
        start = driver.advance(ENGINE, driver.blank(), 329, 1 << 20)
        self.assertEqual(start['steps'], 670358)
        with self.assertRaises(CandidateUndefined):
            driver.advance(ENGINE, start, 1, 1 << 20)
        end = resolve_candidate(driver, ENGINE, start, 1, 1 << 20, 100000, lambda _: None)
        self.assertEqual((end['groups'], end['steps']), (330, 674448))
        machine = TapeMachine(driver.machine)
        exceptional = []
        while machine.steps < end['steps']:
            if machine.head >= 0 and machine.state == 'B' and machine.tape.get(machine.head) == 2:
                exceptional.append((machine.steps, machine.head))
            self.assertTrue(machine.step())
        self.assertEqual(exceptional, [(672396 + i, 34 - i) for i in range(4)])
        self.assertEqual((machine.head, machine.state, machine.tape), (0, end['state'], cells(driver, end)))

    def test_meets_saved_window(self):
        driver = Driver(20)
        # First complete the exceptional 330th period with the original rules.
        start = resolve_candidate(driver, ENGINE, driver.blank(), 330, 1 << 20, 100000, lambda _: None)
        reference = survey.load(ROOT / 'frontiers/runs/window-20.json', 20, driver.machine)
        low, high = 330, 50000
        last = start
        while high - low > 1:
            mid = (high + low) // 2
            candidate = driver.advance(ENGINE, start, mid - 330, 1 << 20)
            if candidate['steps'] > reference['steps']:
                high = mid
            else:
                low, last = mid, candidate
        self.assertLess(reference['steps'] - last['steps'], 10**6)
        tape = cells(driver, last)
        origin = min(tape)
        physical = bytes(tape.get(i, 0) for i in range(origin, max(tape) + 1))
        seed = {**reference, 'steps': last['steps'], 'head': 0, 'state': last['state'],
                'left': origin, 'cells': len(physical),
                'tape_zlib_base64': base64.b64encode(zlib.compress(physical, 9)).decode()}
        got, _ = survey.advance(WINDOW, 20, driver.machine, seed, reference['steps'], 10**6, 7)
        self.assertEqual(got, reference)


if __name__ == '__main__':
    unittest.main()
