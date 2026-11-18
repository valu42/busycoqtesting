"""Single-instruction checks for the line 19/23 launch filter."""
import unittest

from line19_guard_filter import MACHINE, PREFIXES, SAFE, TapeMachine, check_closed, collect, permits_aaa


class GuardFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.heads, cls.words = collect()

    def test_every_completion_and_both_seeds(self):
        check_closed(self.heads, self.words)
        self.assertEqual((len(self.heads), *(len(w) for w in self.words)), (13720, 50, 94))
        prefixes = {r[1:] for _, q, c, r in self.heads if (q, c, r[0]) == ('A', '0', '3')}
        self.assertEqual(prefixes, PREFIXES)
        self.assertEqual({p for p in prefixes if not permits_aaa(p)}, SAFE)
        # An induction certificate missing the g=0 seed must fail its own checker.
        bad = self.heads - {('000', 'B', '0', '00000')}
        with self.assertRaises(ValueError):
            check_closed(bad, self.words)

    def test_literal_strip_transfers(self):
        # Supply the two possible replies to the sole child call. The outer
        # sequence stops as soon as B returns, denying the guard its third A.
        for word in sorted(SAFE):
            for child in 'AB':
                tm = TapeMachine(MACHINE, map(int, word))
                responses, issued = '', ''
                for request in 'BBA':
                    tm.head, tm.state = 0, request
                    while tm.head >= 0:
                        if tm.head == len(word):
                            issued += tm.state
                            tm.head, tm.state = len(word)-1, child
                        self.assertLess(tm.steps, 40)
                        self.assertTrue(tm.step())
                    responses += tm.state
                    if tm.state == 'B':
                        break
                if word == '3000':
                    self.assertEqual((issued, responses), ('', 'B'))
                else:
                    self.assertEqual((issued, responses), ('B', 'AAB' if child == 'A' else 'AB'))

    def test_real_guard_windows(self):
        for control in 'AB':
            tm = TapeMachine(MACHINE)
            tm.state = control
            launches = 0
            for _ in range(30000):
                if tm.state == 'A' and not tm.tape.get(tm.head) and tm.tape.get(tm.head+1) == 3:
                    prefix = ''.join(str(tm.tape.get(tm.head+i, 0)) for i in range(2, 6))
                    self.assertIn(prefix, PREFIXES)
                    launches += 1
                self.assertTrue(tm.step())
            self.assertGreater(launches, 0)


if __name__ == '__main__':
    unittest.main()
