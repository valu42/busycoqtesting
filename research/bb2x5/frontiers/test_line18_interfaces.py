"""Independent finite checks of the line 18 guards, projections and binary carry."""
from itertools import product
import unittest

from line18 import blank_entry, advance
from line18_interfaces import check_rules, explore_guard, horizon, literal, protected_record


class Interfaces(unittest.TestCase):
    def test_guards(self):
        self.assertEqual(check_rules(), 1709)
        # Three cells do allow a spurious A with an arbitrary reply oracle.
        for word in ('131', '132', '133'):
            self.assertIn('A', explore_guard(word)[0])

    def test_binary_tail(self):
        for width in range(1, 7):
            for digits in product(('31', '32'), repeat=width):
                carry = next((i for i, d in enumerate(digits) if d == '32'), width)
                for marker in ('', '3'):
                    word = ''.join(digits) + marker
                    if carry < width:
                        want = '32'*carry + '31' + ''.join(digits[carry+1:]) + marker
                        steps = 4*carry + 3
                    elif marker:
                        want, steps = '32'*(width+1), 4*width + 3
                    else:
                        want, steps = '32'*(width-1) + '31313', 4*width + 11
                    replies, status, tm = literal(word, 'B')
                    self.assertEqual((replies, status, tm.steps), ('B', 'done', steps))
                    self.assertEqual(tm.tape, {i: int(c) for i, c in enumerate(want)})

    def test_binary_reset(self):
        for width in range(5):
            for digits in product(('31', '32'), repeat=width):
                for marker in ('', '3'):
                    word = ''.join(digits) + marker
                    replies, status, _ = literal(word, 'A'+'B'*100)
                    self.assertEqual((replies, status), ('A'*101, 'done'))
                    if word:
                        replies, status, tm = literal(word, 'AA')
                        self.assertEqual((replies, status, tm.head), ('A', 'halt', 0))

    def test_artificial_prefix(self):
        for guard in ('1312', '1331', '1333'):
            prefix = '13313' + guard
            for extension in ('', '4422', '031', '213', '4444'):
                for count in (1, 2, 4, 8):
                    end, output = protected_record(prefix, count)
                    replies, status, tm = literal(prefix + extension, 'A' + 'B'*count)
                    if status == 'halt':
                        self.assertGreaterEqual(tm.head, end)
                    else:
                        self.assertEqual(replies, 'B'*(count+1))
                        self.assertEqual(output, ''.join(str(tm.tape.get(i, 0))
                                                          for i in range(1, 1+len(output))))

    def test_moving_cut(self):
        state = blank_entry()
        for k in range(1, 101):
            next_state = advance(state, k+1)
            for width in (10, len(state['suffix'])):
                projection = protected_record(state['suffix'][:width], 1 << (k-1))
                if projection is not None:
                    self.assertTrue(next_state['suffix'].startswith(projection[1]))
            state = next_state
        rows = horizon(101, state['suffix'])
        self.assertGreater(len(rows), 1)
        self.assertEqual(rows[0][0], 101)


if __name__ == '__main__':
    unittest.main()
