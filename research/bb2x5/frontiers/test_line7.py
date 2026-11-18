"""Check batched suffix calls, including interrupted nested calls, against literal steps."""
import itertools
import random
import unittest

from line7 import Calls, HALT, MACHINE, ROOT, snapshot
from prior_sweeps import TapeMachine
import survey


class Line7Tests(unittest.TestCase):
    def check_suffix(self, word, state, n):
        m = TapeMachine(MACHINE, word)
        done, response = 0, 'B'
        for _ in range(n):
            m.head, m.state = 0, state
            while m.head >= 0 and m.step():
                self.assertLess(m.steps, 5_000_000)
            response = HALT if m.head >= 0 else m.state
            if response != 'B':
                break
            done += 1
        worker = Calls(word)
        self.assertEqual(worker.run(worker.many(0, state, n)), (done, response))
        self.assertEqual(worker.steps, m.steps)
        self.assertEqual({i: v for i, v in enumerate(worker.tape) if v}, m.tape)
        self.assertEqual(worker.halt_cell, m.head if response == HALT else None)
        return response

    def test_suffixes_and_exceptional_replies(self):
        seen = set()
        for length in range(4):
            for word in itertools.product(range(5), repeat=length):
                for state in 'AB':
                    seen.add(self.check_suffix(word, state, 5))
        self.assertEqual(seen, {'A', 'B', HALT})
        rng = random.Random(7)
        for _ in range(150):
            ordinary = [rng.choice((2, 4)) for _ in range(rng.randrange(7, 13))]
            tail = [rng.randrange(5) for _ in range(3)]
            self.check_suffix(ordinary + tail, rng.choice('AB'), rng.randrange(1, 8))
        for tail in ((1,), (0,), (3, 1), (3, 3, 1)):
            self.check_suffix((2,)*8 + tail, 'A', 2)

    def test_raw_checkpoints(self):
        literal, vm = TapeMachine(MACHINE), Calls()
        for epoch in range(1, 19):
            self.assertTrue(vm.epoch())
            state = snapshot(epoch, vm)
            while literal.steps < vm.steps:
                self.assertTrue(literal.step())
            self.assertEqual((literal.state, literal.head), ('A', -epoch))
            self.assertEqual(literal.tape, {1-epoch+i: s for i, s in enumerate(vm.tape) if s})
            self.assertEqual(int(state['steps_hex'], 16), literal.steps)
        ref = survey.load(ROOT/'frontiers/runs/window-07.json', 7, MACHINE)
        while True:
            epoch += 1
            before = snapshot(epoch-1, vm)
            self.assertTrue(vm.epoch())
            if vm.steps >= ref['steps']:
                break
        # Start the independently implemented moving-window engine at the last
        # boundary before its stored 10^11-step run, then compare the complete tapes.
        import os
        from pathlib import Path
        rows = ['unknown 0', MACHINE, f"{int(before['steps_hex'],16)} {before['head']} 0"]
        pos = before['word_left']
        for symbol, group in itertools.groupby(before['word']):
            n = sum(1 for _ in group)
            if symbol != '0':
                rows.append(f'{pos} {n} {symbol}')
            pos += n
        seed, _ = survey.pack(7, MACHINE, '\n'.join(rows))
        engine = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))
        got, _ = survey.advance(engine, 7, MACHINE, seed, ref['steps'], 10**10, 8)
        self.assertEqual(got, ref)


if __name__ == '__main__':
    unittest.main()
