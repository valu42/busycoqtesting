"""Differential tests for the physical line 5 clock, dense sums, and native replay."""
import os
from pathlib import Path
import unittest

from line5_timed import ROOT, State, advance, blank, load, native, scalar, step, verify_local_rules
from prior_sweeps import audit_arithmetic_transition


class TimedTests(unittest.TestCase):
    def test_universal_rules_and_literal_durations(self):
        verify_local_rules()
        for tag in 'AB':
            for a in range(10):
                for b in range(15):
                    start = State(tag, a, b)
                    end, elapsed, events = step(start)
                    pos, expected_time = start, 0
                    for _ in range(events):
                        target = scalar(pos)
                        target_tuple = None if target is None else (target.tag, target.a, target.b)
                        expected_time += audit_arithmetic_transition((pos.tag, pos.a, pos.b), target_tuple)
                        pos = target
                    self.assertEqual((end, elapsed), (pos, expected_time))

    def test_continuation_of_published_clock(self):
        saved = load(ROOT/'frontiers/runs/line5-timed.json')
        n = saved['rounds']
        direct = advance(saved, n+3)
        self.assertEqual(direct, advance(advance(saved, n+1), n+3))
        self.assertGreater(int(direct['steps_hex'], 16), int(saved['steps_hex'], 16))

    def test_native_and_partitioned_replays(self):
        engine = Path(os.environ.get('BB25_TIME5', '/tmp/bb25-time5'))
        for n in (0, 1, 9, 71, 512, 10000):
            self.assertEqual(native(engine, n), advance(advance(blank(), n//3), n))


if __name__ == '__main__':
    unittest.main()
