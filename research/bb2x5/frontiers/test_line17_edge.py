"""Check output-rank inversion, a universal edge bound and conditional branches."""
import itertools
import os
from pathlib import Path
import subprocess
import unittest

import line17
from line17_edge import (DATA, DIGITS, LOCKED, ROOT_PERIOD, ZERO, bits, branch_witnesses,
                         cut_limits, edge_bound, forced_output, initial, packed_source_slot,
                         possible_symbols, source_slot, suffix_event)
from prior_frontier import force_prefix, mark_step, marks_on_word, periodic_marks, pulse_on_tail


PACKED = Path(os.environ.get('BB25_PACK17', '/tmp/bb25-packed17')).resolve()


class EdgeTests(unittest.TestCase):
    def test_digit_count_and_zero_completion(self):
        for v, p in itertools.product(range(3), range(2)):
            for word in itertools.product((0, 1), repeat=8):
                trit, pending = v, p
                count = compound = 0
                for bit in word:
                    if bit and pending:
                        break
                    compound += bool(bit or pending)
                    trit, pending, emitted = mark_step(trit, pending, bit)
                    count += len(emitted)
                else:
                    self.assertEqual(3*count+trit, v+8+4*compound)
                    _, minimum = marks_on_word((v, p), bytes(8))
                    self.assertLessEqual(len(minimum), count)

    def test_corrupted_clock_components(self):
        epochs = 100
        word = ROOT_PERIOD*epochs
        rows = []
        for i in range(len(DIGITS)):
            rows.append(line17.literal_counts(initial(i), word))
            _, word = marks_on_word(initial(i), word)
        line17.check_pulse_counts(epochs, DIGITS, rows)
        rows[0].calls += 1
        with self.assertRaises(ValueError):
            line17.check_pulse_counts(epochs, DIGITS, rows)
        rows[0].calls -= 1
        rows[0].interior += 2
        with self.assertRaises(ValueError):
            line17.check_pulse_counts(epochs, DIGITS, rows)

    def test_rank_at_chunk_and_period_boundaries(self):
        epochs = 130
        for depth in (1, 2, 7, 11):
            labels = [(j, bit) for j, bit in enumerate(ROOT_PERIOD*epochs, 1)]
            for i in range(depth):
                v, p = initial(i)
                child = []
                for j, bit in labels:
                    v, p, out = mark_step(v, p, bit)
                    child.extend((j, b) for b in out)
                labels = child
            for rank in (1, len(labels)//2, len(labels), len(labels)+1):
                for limit in (16, 2**16):
                    result = subprocess.check_output(
                        [str(PACKED), str(epochs), str(limit), '10000', 'select', str(rank)],
                        input=DATA[:2*depth], text=True)
                    self.assertEqual(result.strip(), str(labels[rank-1][0]) if rank <= len(labels) else 'none')
        for rank in (1, 10**150+3):
            expected = source_slot(initial(0), b'', ROOT_PERIOD, rank)
            self.assertEqual(packed_source_slot(PACKED, 65536, 1, rank), expected)

    def test_bound_and_attainability(self):
        known = LOCKED
        for i in range(402, len(DIGITS)):
            target = forced_output(initial(i), known)
            # Independent universal-prefix checker from the initial register proof.
            force_prefix(*initial(i), tuple(known), tuple(target))
            known = target
        limits = cut_limits()
        when, row = suffix_event(403, LOCKED, ZERO)
        self.assertEqual((when, row[-13:]), (81526541, '4444040444444'))
        self.assertEqual(limits[403], when)
        for i in range(53, 403):
            self.assertEqual(limits[i], 3*limits[i+1]-49)
        self.assertEqual(edge_bound(), edge_bound(53, PACKED, 2**20))
        self.assertEqual(suffix_event(403, b'', bits('000010'))[0], 9058530)

    def test_cached_period_ranks_and_clocks(self):
        # The narrow pass reaches cut 50 with a repeated 83,556-slot word.
        # The larger word budget with zero finite slots requires a wholly
        # periodic transfer through cut 57, independent of the period cache.
        for start in (0, 123456789):
            prefix = line17.replay(start, 22)['register'][:2*57]
            def run(bits, work, *mode):
                return subprocess.check_output([str(PACKED), str(10**16), str(bits), str(work), *mode],
                                               input=prefix, text=True)
            reference = run(2**23, 0)
            self.assertEqual(run(2**17, 20000000), reference)
            size = int(reference.splitlines()[-1].split()[2])
            for rank in (1, size//3, size-1, size, size+1):
                self.assertEqual(run(2**17, 20000000, 'select', str(rank)),
                                 run(2**23, 0, 'select', str(rank)))

    def test_three_branches_against_literal_suffix(self):
        cases = list(branch_witnesses())
        self.assertEqual([(g, n, w[0]) for g, n, w in cases],
                         [(5, 165, '0'), (7, 3641, '4'), (8, 461, '1')])
        for gap, stop, word in cases:
            row = DATA[2*403:]+'2'
            pending = initial(403)[1]
            for t in range(1, stop+1):
                bit = t in (5, 11, 17, 23) or (t >= 28 and (t-28) % gap == 0)
                self.assertFalse(pending and bit)
                v = '102'.index(row[0])
                hit, row = pulse_on_tail(row, pending or bit)
                pending = (pending or bit) and v != 0
                self.assertEqual(hit, t == stop)
            self.assertEqual(row[-13:], word)
            supplied = [5, 11, 17, 23]+list(range(28, stop+1, gap))
            self.assertEqual(possible_symbols(stop, supplied)[1], (int(word[0]),))

    def test_two_decisive_bits_and_truncated_mark_streams(self):
        for tail in itertools.product((0, 1), repeat=4):
            prefix = bits('01000000')+bytes(tail)
            positions = [i for i, b in enumerate(prefix, 1) if b]
            if any(b-a < 3 for a, b in zip(positions, positions[1:])):
                continue
            wanted = '1' if tail[0] else '0' if tail[1] else '4'
            at, row = suffix_event(418, prefix, ZERO)
            self.assertLessEqual(at, 12)
            self.assertEqual(row[-13], wanted)
        self.assertEqual(cut_limits(418, 10)[403], 52828727)
        self.assertEqual(possible_symbols(38479820, [5, 11, 17, 23]), (9, (0, 4)))
        self.assertEqual(possible_symbols(52828727, [5, 11, 17, 23]), (10, (4,)))
        for start in (0, 1, 70, 1000):
            marks = [i for i in (5, 11, 17, 23) if i <= start]
            self.assertEqual(possible_symbols(start, marks)[0], 0)
        minimum = (LOCKED, ZERO)
        infinite = (b'', bits('000010'))
        for i in range(403, 406):
            minimum = periodic_marks(initial(i), *minimum)
            infinite = periodic_marks(initial(i), *infinite)
        self.assertEqual(minimum, (bits('0001'), ZERO))
        self.assertEqual(infinite, minimum)


if __name__ == '__main__':
    unittest.main()
