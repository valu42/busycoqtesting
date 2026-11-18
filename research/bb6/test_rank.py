"""Regression checks for blank entry, reflection, changed slots and probe cutoffs."""

import unittest

from rank import Match, parse_table, probe, related_tables, review_order
from tracker import load_register


class RankingTests(unittest.TestCase):
    def test_halt_exactly_at_budget(self):
        table = parse_table("1LB---_------_------_------_------_------")
        self.assertIsNone(probe(table, 0).halt)
        run = probe(table, 1)
        self.assertEqual((run.halt, run.edge, run.first_read[2]), (1, "L/B/1000", 1))

    def test_edge_period_needs_evidence_in_both_halves(self):
        drift = parse_table("1RA---_------_------_------_------_------")
        self.assertEqual(probe(drift, 23).period, 0)
        run = probe(drift, 64)
        self.assertEqual((run.period, run.support, run.edge), (1, 61, "R/A/1111"))

    def test_peer_entry_and_changed_instruction(self):
        rows = load_register()
        tables = {n: parse_table(rows[n - 1]["machine"]) for n in (133, 247, 448, 581, 598)}
        families, matches = related_tables(tables, {581, 598}, {133, 247, 448})
        self.assertIn(Match(581, 2, True, None, None), matches[133])
        self.assertIn(Match(598, 0, False, 10, (0, 1, 3)), matches[448])
        self.assertIn(247, families[448])
        self.assertNotIn(598, families[448])
        self.assertEqual(probe(tables[448], 303).first_read[10], 303)

    def test_review_batches_and_direct_theorems(self):
        rows = {
            1: {"status": "SIMULATED_HALT", "source": "log"},
            2: {"status": "HALT_PR", "source": "pr-a"},
            3: {"status": "NONHALT_PR", "source": "pr-b"},
            4: {"status": "NONHALT_PR", "source": "pr-b"},
            5: {"status": "EQUIVALENCE_PR", "source": "pr-c"},
        }
        sources = {n: {} for n in rows}
        self.assertEqual(review_order(rows, rows, sources), [3, 4, 2, 1, 5])
        sources[2]["replay"] = True
        self.assertEqual(review_order(rows, rows, sources), [2, 3, 4, 1, 5])


if __name__ == "__main__":
    unittest.main()
