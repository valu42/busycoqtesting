"""Compare the line 3 clock and tape against single instructions."""
from itertools import product
import unittest

import survey
from line3_timed import MIX, ROOT, TapeMachine, advance, blank, snapshot
from mixed_and_sweeps import canonical, next_zero, skip


class TimedTests(unittest.TestCase):
    def test_token_clocks(self):
        # Marker-bearing and partial binary registers include all-ones carries.
        for prefix in ([1, 3], [1, 3, 2, 3, 3], [4, 2, 3, 2], [4, 3, 3]):
            for length in range(1, 5):
                for tokens in product((None, 0, 1, 2), repeat=length):
                    suffix = []
                    for digit in tokens:
                        suffix.extend([4] if digit is None else [2, (2, 0, 4)[digit]])
                    word = prefix + suffix + [1]
                    for cap in (1, None):
                        raw = TapeMachine(MIX, word, len(prefix))
                        fast = TapeMachine(MIX, word, len(prefix))
                        elapsed = skip(fast, cap, exact=True)
                        for _ in range(elapsed):
                            self.assertTrue(raw.step())
                        self.assertEqual((raw.head, raw.state, raw.tape),
                                         (fast.head, fast.state, fast.tape), (prefix, tokens, cap))

    def test_blank_trajectory_and_resume(self):
        # Contains the nontrivial reset at step 59,171 and a 531,433-probe batch.
        end = advance(blank(), 10)
        raw = TapeMachine(MIX)
        elapsed = int(end['steps_hex'], 16)
        self.assertEqual(elapsed, 4310726)
        for _ in range(elapsed):
            self.assertTrue(raw.step())
        self.assertEqual(snapshot(raw, 10, 'unknown'), end)
        self.assertEqual(advance(advance(blank(), 9), 10), end)

    def test_halting_reset(self):
        m = canonical(19, 2, 1)
        # Same normal family as the blank checkpoints, with a known A1 halt.
        m.steps = 20
        p = snapshot(m, 0, 'unknown')
        end = advance(p, 1)
        while m.step():
            pass
        self.assertEqual(snapshot(m, 0, 'halt'), end)
        self.assertEqual(advance(end, 1), end)

    def test_existing_window_meets_blank_replay(self):
        old = survey.load(ROOT/'frontiers/runs/window-03.json', 3, MIX)
        raw = TapeMachine(MIX, survey.verify_state(old, MIX), old['head'], old['left'])
        raw.state = old['state']
        normal, elapsed, _ = next_zero(raw, exact=True)
        self.assertEqual(normal, (45571118, 16, 1, 0))
        raw.steps = old['steps'] + elapsed
        self.assertEqual(snapshot(raw, 14, 'unknown'), advance(blank(), 14))


if __name__ == '__main__':
    unittest.main()
