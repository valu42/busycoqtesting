"""Compare line 18's exact records and suffix batches with physical TM tapes."""
import base64
from itertools import product
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zlib

from checkpoints import ROOT
from line18 import MACHINE, Suffix, advance, blank_entry, load, save
from line18_header import verify
from line18_replies import audit
from prior_sweeps import TapeMachine
import survey


def physical(p):
    word = '134' + '313'*p['record'] + p['suffix']
    tm = TapeMachine(MACHINE, map(int, word), head=p['head'], left=p['head'] + 1)
    tm.steps = int(p['steps_hex'], 16)
    return tm


class Line18Tests(unittest.TestCase):
    def test_exception_observed_on_the_blank_tape(self):
        seed = blank_entry()
        doc = audit(seed, 8)
        self.assertEqual(doc['internal_A_replies_at_batch_boundaries'], 7)
        self.assertEqual(doc['outer_B_requests_returning_B_hex'], '0xff')
        first = doc['witnesses']['first_occupied_strip']
        self.assertEqual((first['record'], first['coordinate'], first['before'], first['after']),
                         (8, 31, '33132', '13231'))
        tm = physical(advance(seed, first['record']))
        stop = int(advance(seed, first['record']+1)['steps_hex'], 16)
        left, width = first['coordinate'], len(first['before'])

        def strip():
            return ''.join(str(tm.tape.get(i, 0)) for i in range(left, left+width))

        while tm.steps < stop:
            old = tm.head
            self.assertTrue(tm.step())
            if (old == left-1 and tm.head == left and tm.state == first['entry_state']
                    and strip() == first['before']):
                for _ in range(first['steps']):
                    self.assertTrue(tm.step())
                self.assertEqual((tm.head, tm.state, strip()), (left-1, 'A', first['after']))
                return
        self.fail('literal blank orbit did not visit the reported witness')

    def test_one_cell_at_record_9333(self):
        seed = load(ROOT/'frontiers/runs/line18-returns.json')
        cut = 9347
        for altered in (False, True):
            tm = physical(seed)
            self.assertEqual(''.join(str(tm.tape[cut+i]) for i in range(6)), '131313')
            if altered:
                tm.tape[cut+2] = 3
            calls, replies = [], []
            for offset in range(1, 252200):
                old = tm.head
                self.assertTrue(tm.step())
                if (old, tm.head) == (cut-1, cut):
                    calls.append(tm.state)
                elif (old, tm.head) == (cut, cut-1):
                    replies.append((offset, tm.state))
                if len(replies) == 3:
                    break
            self.assertEqual(calls, list('ABB'))
            if altered:
                self.assertEqual(replies, [(252139, 'B'), (252189, 'B')])
                self.assertEqual((tm.head, tm.state, tm.tape[tm.head]), (9352, 'A', 4))
                self.assertFalse(tm.step())
            else:
                self.assertEqual(replies, [(252139, 'B'), (252175, 'B'), (252181, 'B')])

    def test_literal_blank_records(self):
        verify()
        tm = TapeMachine(MACHINE)
        seed = blank_entry()
        for k in range(1, 13):
            fast = physical(advance(seed, k))
            while tm.steps < fast.steps:
                self.assertTrue(tm.step())
            self.assertEqual((tm.head, tm.state, tm.tape), (fast.head, fast.state, fast.tape))

    def test_suffix_batches(self):
        # Exercise both widths, phases of the digit, a variable child, and
        # its first A reply inside a batch. Compare every written symbol.
        outcomes = set()
        for prefix in ('31', '32', '3133', '3233', '3133133'):
            for tail in product(range(5), repeat=2):
                word = [int(c) for c in prefix] + list(tail)
                for count in (1, 2, 7):
                    raw = TapeMachine(MACHINE, word)
                    done, reply = 0, 'B'
                    while done < count:
                        raw.head, raw.state = 0, 'B'
                        while raw.head >= 0 and raw.step():
                            self.assertLess(raw.steps, 10000)
                        if raw.head >= 0 or raw.state == 'A':
                            reply = 'halt' if raw.head >= 0 else 'A'
                            break
                        done += 1
                    machine = Suffix(word, 10000)
                    outcomes.add(reply)
                    if reply == 'halt':
                        with self.assertRaisesRegex(RuntimeError, 'undefined'):
                            machine.b_calls(0, count)
                        continue
                    self.assertEqual(machine.b_calls(0, count), (done, reply), (word, count))
                    self.assertEqual(machine.steps, raw.steps, (word, count))
                    self.assertEqual({i: c for i, c in enumerate(machine.cells) if c}, raw.tape)
        self.assertEqual(outcomes, {'A', 'B', 'halt'})

    def test_checkpoint_continuation(self):
        with TemporaryDirectory() as temp:
            path = Path(temp)/'state.json'
            save(path, advance(blank_entry(), 26))
            self.assertEqual(advance(load(path), 81), advance(blank_entry(), 81))

    def test_matches_prior_window(self):
        old = survey.load(ROOT/'frontiers/runs/window-18.json', 18, MACHINE)
        tm = physical(advance(blank_entry(), 27))
        self.assertEqual(tm.steps, 9306778039)
        left = min(tm.tape)
        cells = bytes(tm.tape.get(i, 0) for i in range(left, max(tm.tape) + 1))
        seed = {**old, 'head': tm.head, 'state': tm.state, 'steps': tm.steps,
                'left': left, 'cells': len(cells),
                'tape_zlib_base64': base64.b64encode(zlib.compress(cells, 9)).decode()}
        engine = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))
        got, _ = survey.advance(engine, 18, MACHINE, seed, old['steps'], 40000000, 8)
        self.assertEqual(got, old)


if __name__ == '__main__':
    unittest.main()
