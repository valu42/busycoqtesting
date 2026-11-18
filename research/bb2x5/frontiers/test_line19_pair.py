"""Check the tape conjugacy and the parity guard against literal instructions."""
import sys
import unittest

from checkpoints import ROOT
from line19_pair import FREQUENT_PREFIX, verify_long_guard, DIGITS, MACHINES, STATES, translate_checkpoint, verify_parity_guard, verify_tables
import survey
sys.path.insert(0, str(ROOT))
from prior_sweeps import TapeMachine


def restore(payload):
    cells = survey.verify_state(payload, payload['machine'])
    tm = TapeMachine(payload['machine'], cells, payload['head'], payload['left'])
    tm.state, tm.steps = payload['state'], payload['steps']
    return tm


class ReflectedGuards(unittest.TestCase):
    def assert_reflection(self, a, b):
        self.assertEqual((a.steps, -a.head, STATES[a.state]), (b.steps, b.head, b.state))
        self.assertEqual({-x: DIGITS[s] for x, s in a.tape.items()}, b.tape)

    def test_both_blank_seeds(self):
        verify_tables()
        for state in 'AB':
            a, b = (TapeMachine(code) for code in MACHINES.values())
            a.state, b.state = state, STATES[state]
            for t in range(20001):
                if t in (0, 1, 256, 20000):
                    self.assert_reflection(a, b)
                self.assertTrue(a.step() and b.step())

    def test_window_continuations(self):
        for line, other in ((19, 23), (23, 19)):
            p = survey.load(ROOT/'frontiers'/'runs'/f'window-{line}.json', line, MACHINES[line])
            q = translate_checkpoint(p, other)
            self.assertEqual(p, translate_checkpoint(q, line))
            a, b = restore(p), restore(q)
            for _ in range(20000):
                self.assertTrue(a.step() and b.step())
            self.assert_reflection(a, b)

    def test_one_cell_flips_an_observed_third_call(self):
        # Normalized coordinates for the two physical orbits.
        cases = (('A', 716152, -168, 31, 0, (49, 55, 235), 295),
                 ('B', 52, -4, 4, 3, (3, 13, 21), 51))
        for seed, clock, x, offset, digit, ordinary, altered in cases:
            tm = TapeMachine(MACHINES[19])
            tm.state = seed
            for _ in range(clock):
                self.assertTrue(tm.step())
            self.assertEqual((tm.head, tm.state, tm.tape.get(x, 0), tm.tape[x+1]), (x, 'A', 0, 3))
            self.assertEqual(tm.tape[x+offset], 2)
            for change in (False, True):
                run = TapeMachine(MACHINES[19])
                run.tape, run.head = tm.tape.copy(), x
                if change:
                    if digit:
                        run.tape[x+offset] = digit
                    else:
                        del run.tape[x+offset]
                requests, replies = [], []
                while len(replies) < 3:
                    old = run.head
                    self.assertLessEqual(run.steps, altered)
                    self.assertTrue(run.step())
                    if (old, run.head) == (x+1, x+2):
                        requests.append(run.state)
                    if (old, run.head) == (x+2, x+1):
                        replies.append((run.steps, run.state))
                self.assertEqual(''.join(requests), 'BBA')
                times = (*ordinary[:2], altered if change else ordinary[2])
                self.assertEqual(replies, list(zip(times, 'AAA' if change else 'AAB')))
                if change:
                    self.assertTrue(run.step() and run.step())
                    self.assertEqual((run.head, run.state, run.tape[run.head]), (x+1, 'A', 3))
                    self.assertFalse(run.step())

    def test_arbitrarily_long_common_launch_prefix(self):
        for m in range(4, 62):
            word = '0330' + '2'*m + '0'
            for exterior in ('', '4143'):
                tm = TapeMachine(MACHINES[19], map(int, word + exterior))
                for _ in range(2*m + (37 if m % 2 else 15)):
                    self.assertGreaterEqual(tm.head, 0)
                    self.assertLess(tm.head, len(word))
                    self.assertTrue(tm.step())
                self.assertEqual((tm.state, tm.head), ('A', 1 if m % 2 else -1))
                if m % 2:
                    self.assertFalse(tm.step())

    def test_frequent_guard_class_has_both_controls(self):
        verify_long_guard()
        for m in (11, 12, 13, 42, 87, 136):
            word = FREQUENT_PREFIX + '2'*m + '0'
            tm = TapeMachine(MACHINES[19], map(int, word + '434'))
            for _ in range(2*m + (205 if m % 2 else 471)):
                self.assertGreaterEqual(tm.head, 0)
                self.assertLess(tm.head, len(word))
                self.assertTrue(tm.step())
            self.assertEqual((tm.head, tm.state), (1 if m % 2 else -1, 'A'))
            if m % 2:
                self.assertFalse(tm.step())

    def test_literal_parity_guards(self):
        verify_parity_guard()
        for m in range(1, 21):
            # B on 0 replies A in one step. B on 20 replies B in three.
            for tail, cost, returns_a in (('0', 1, True), ('20', 3, False)):
                halted = returns_a == (m % 2 == 0)
                word = list(map(int, '032' + '2'*(m-1) + tail + '413'))
                a = TapeMachine(MACHINES[19], word)
                b = TapeMachine(MACHINES[23], [DIGITS[s] for s in reversed(word)], left=1-len(word))
                b.state = 'B'
                steps = 2*m + (8 if halted else 6) + cost
                for _ in range(steps):
                    self.assertGreaterEqual(a.head, 0)
                    self.assertTrue(a.step() and b.step())
                self.assert_reflection(a, b)
                self.assertEqual((a.head, a.state), (1 if halted else -1, 'A'))
                if halted:
                    self.assertEqual((a.tape[a.head], b.tape[b.head]), (3, 4))
                    self.assertFalse(a.step() or b.step())


if __name__ == '__main__':
    unittest.main()
