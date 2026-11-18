"""Compare packed guard recognition with chronological, literal suffix calls."""
from collections import Counter
import os
from pathlib import Path
import sys
import unittest

from checkpoints import ROOT
import spaghetti_guard as sg
import survey

sys.path.insert(0,str(ROOT))
from prior_sweeps import TapeMachine

ENGINE = Path(os.environ.get('BB25_SPAGHETTI','/tmp/bb25-spaghetti'))


def literal(seed, target):
    tm = TapeMachine(sg.MACHINES[19])
    tm.state = seed
    counts = {d:Counter() for d in sg.DIGITS}
    pending, words, word_counts, fresh_counts, visited = {}, {}, {}, Counter(), set()
    previous = candidate = request = first = longest = None
    while tm.steps < target:
        x, t = tm.head, tm.steps
        if request is not None:
            assert (x,tm.state) == request
            request = None
        if candidate is not None:
            seed_time, cell, word, fresh = candidate
            digit = int(word[0])
            assert (x,t,tm.state,tm.tape[x]) == (cell,seed_time,'B',3)
            pending[x] = {'cell':x,'entry':t,'suffix_digit':digit,'returns':[]}
            words[x] = word
            word_counts.setdefault(word, Counter())['B3'] += 1
            fresh_counts[word] += int(fresh)
            counts[digit]['B3'] += 1
            request = x+1,'B'
            candidate = None
        # An open call returns exactly when the head steps back onto its parent.
        if previous == x+1 and x in pending:
            g = pending[x]
            s = len(g['returns'])
            assert tm.tape.get(x,0) == s
            if s < 2 and tm.state == 'A':
                request = x+1,'BBA'[s+1]
            channel = 'A'*s+tm.state
            counts[g['suffix_digit']][channel] += 1
            word_counts[words[x]][channel] += 1
            g['returns'].append(t)
            if s == 2:
                if first is None:
                    first = g
                if longest is None or t-g['returns'][1] > longest['returns'][2]-longest['returns'][1]:
                    longest = g
            if s == 2 or tm.state == 'B':
                del pending[x], words[x]
        if tm.state == 'A' and tm.tape.get(x,0) == 0 and tm.tape.get(x+1,0) == 3:
            word = ''.join(str(tm.tape.get(x+j,0)) for j in range(2,6))
            candidate = t+1, x+1, word, x not in visited
        visited.add(x)
        previous = x
        if not tm.step():
            break
    return tm, counts, word_counts, fresh_counts, first, longest, [pending[x] for x in sorted(pending)]


class SpaghettiTests(unittest.TestCase):
    def test_guard_antecedents(self):
        sg.verify_antecedents()
        sg.verify_short_third_calls()

    def test_synthetic_interior_suffix(self):
        # Start the six consecutive calls against one finite physical suffix.
        m = TapeMachine(sg.MACHINES[19], map(int,'2202000'))
        for state in 'BBABBA':
            m.head, m.state = 0, state
            while m.head>=0:
                self.assertLess(m.head,7)
                self.assertTrue(m.step())
            self.assertEqual(m.state,'A')

    def test_literal_guard_crossings(self):
        for line,seed in ((19,'A'),(23,'B')):
            for target in (0,54,97,99,110,117,1000000):
                with self.subTest(line=line,target=target):
                    p = sg.replay(ENGINE,line,target,profile=True)
                    tm,counts,word_counts,fresh_counts,first,longest,pending = literal(seed,target)
                    normalized = sg.translate_checkpoint(p['configuration'],19)
                    cells = survey.verify_state(normalized,sg.MACHINES[19])
                    tape = {normalized['left']+i:s for i,s in enumerate(cells) if s}
                    self.assertEqual((tm.steps,tm.head,tm.state,tm.tape),
                                     (normalized['steps'],normalized['head'],normalized['state'],tape))
                    self.assertEqual((first,longest,pending),
                                     (p['first_third_return'],p['longest_third_call'],p['open_guards']))
                    got = {w:Counter(c) for w,c in p['counts_by_launch_word'].items()}
                    self.assertEqual(word_counts,got)
                    self.assertEqual(dict(fresh_counts),p['fresh_left_launches_by_word'])
                    for d in sg.DIGITS:
                        self.assertEqual(counts[d],Counter(p['counts_by_suffix_digit'][str(d)]))

    def test_independent_window_endpoints(self):
        for line in sg.MACHINES:
            expected = survey.load(ROOT/f'frontiers/runs/window-{line}.json',line,sg.MACHINES[line])
            self.assertEqual(sg.replay(ENGINE,line,expected['steps'])['configuration'],expected)


if __name__ == '__main__':
    unittest.main()
